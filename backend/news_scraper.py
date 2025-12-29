# =============================================================================
# backend/news_scraper.py — TOMSARKGH EVENT SCRAPER
# =============================================================================
# Scrape events from tomsarkgh.am with proper categories for AskYerevan
# Categories in DB: culture, events, city, holiday_events, important (manual)
# =============================================================================

import re
from datetime import date, timedelta
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from backend.database import save_news
from backend.utils.logger import logger

# =============================================================================
# CONSTANTS
# =============================================================================

BASE_TOMSARKGH_URL = "https://www.tomsarkgh.am"
HEADERS = {
    "User-Agent": "AskYerevanBot/1.0 (+https://askyerevan.am)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Tomsarkgh EventType IDs → AskYerevan categories
TOMSARKGH_CATEGORIES = {
    # 🎉 ՄԻՋՈՑԱՌՈՒՄՆԵՐ (events)
    16: "events",   # Կրկես
    54: "events",   # Stand‑up
    31: "events",   # Ակումբ/փաբ
    21: "events",   # Պար
    6:  "events",   # Կինո

    # ⛄ ՏՈՆԵՐ (holiday_events)
    41: "holiday_events",

    # 🏛️ ՄՇԱԿՈՒՅԹ (culture)
    1:  "culture",  # Թատրոն
    12: "culture",  # Օպերա‑բալետ
    2:  "culture",  # Կոնցերտ
    10: "culture",  # Պոպ

    # 🏙️ ՔԱՂԱՔԱՅԻՆ (city)
    7: "city",      # Other events
}

# =============================================================================
# HELPERS
# =============================================================================

def _safe_text(el) -> str:
    """Extract clean text from BeautifulSoup element."""
    return el.get_text(strip=True) if el else ""


def _full_text(soup: BeautifulSoup) -> str:
    """Full visible text of the page (for regex fallbacks)."""
    return soup.get_text(separator="\n", strip=True)


# =============================================================================
# LIST PAGE → EVENT URLS
# =============================================================================

def fetch_tomsarkgh_events(event_type: int, days_ahead: int = 7) -> List[str]:
    """
    Fetch event URLs from Tomsarkgh list endpoint by EventType and date range.
    Uses /list?EventType[]=...&startFrom=..&startTo=...
    """
    today = date.today()
    start = today.strftime("%m/%d/%Y")
    end = (today + timedelta(days=days_ahead)).strftime("%m/%d/%Y")

    params = {
        "EventType[]": str(event_type),
        "startFrom": start,
        "startTo": end,
    }

    try:
        logger.info(f"📋 Tomsarkgh list: type={event_type}, {start}→{end}")
        resp = requests.get(
            f"{BASE_TOMSARKGH_URL}/list",
            params=params,
            timeout=15,
            headers=HEADERS,
        )
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"❌ Tomsarkgh list error (type={event_type}): {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    links: List[str] = []

    # ցանկացած event link՝ /hy/event/XXXXX...
    for a in soup.select("a[href*='/hy/event/']"):
        href = a.get("href", "").strip()
        if not href or "/hy/event/" not in href:
            continue
        full_url = href if href.startswith("http") else BASE_TOMSARKGH_URL + href
        if full_url not in links:
            links.append(full_url)

    logger.info(f"✅ Found {len(links)} events for type={event_type}")
    # սահմանափակենք, որ Render‑ը չպայթի
    return links[:20]


# =============================================================================
# EVENT PAGE PARSER
# =============================================================================

def _parse_event_datetime(soup: BeautifulSoup) -> (str, str):
    """
    Parse event_date (YYYY-MM-DD կամ human string) և event_time ("14:00" կամ "14:00, 18:00").
    Նախընտրում ենք schema.org meta=startDate, հետո՝ fallback regex.
    """
    # primary: <meta itemprop="startDate" content="2025-12-30 14:00">
    meta = soup.select_one("meta[itemprop='startDate']")
    event_date = ""
    event_time = ""

    if meta and meta.get("content"):
        raw = meta["content"].strip()  # "2025-12-30 14:00"
        # բաժանել օրը և ժամը
        parts = raw.split()
        if len(parts) >= 1:
            event_date = parts[0]
        if len(parts) >= 2:
            event_time = parts[1]

    # fallback՝ regex ամբողջ տեքստի վրա
    txt = _full_text(soup)
    if not event_date:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", txt)
        if m:
            event_date = m.group(1)
    if not event_time:
        m = re.search(r"(\d{1,2}[:․]\d{2})", txt)
        if m:
            event_time = m.group(1).replace("․", ":")

    return event_date[:32], event_time[:32]


def _parse_event_venue(soup: BeautifulSoup) -> str:
    """
    Parse venue_hy՝ հիմնականում .occurrence_venue span[itemprop='name'].
    Օրինակ՝ «Ուլիխանյան ակումբ»։
    """
    el = soup.select_one(".occurrence_venue span[itemprop='name']")
    if el:
        return _safe_text(el)[:100]

    # fallback: event_resume / description‑ից venue նշում
    txt = _full_text(soup)
    m = re.search(
        r"(թատրոն|ակումբ|ջազ ակումբ|համերգասրահ|cinema|hall)[^\n]{0,80}",
        txt,
        re.IGNORECASE,
    )
    return m.group(0).strip()[:100] if m else ""


def _parse_event_price(soup: BeautifulSoup) -> str:
    """
    Parse price_hy՝ նախընտրում ենք schema.org Offer price meta, հետո՝ տեքստային regex.
    """
    meta_price = soup.select_one("span[itemprop='offers'] meta[itemprop='price'], meta[itemprop='price']")
    if meta_price and meta_price.get("content"):
        # օրինակ "5000.00" → "5000"
        raw = meta_price["content"].strip()
        m = re.match(r"(\d+)", raw)
        if m:
            return m.group(1)

    # fallback՝ ամբողջ description‑ից
    txt = _full_text(soup)
    m = re.search(r"(\d{3,}(?:[-–]\d{3,})?)\s*(?:դր\.?|դրամ|AMD)", txt)
    return m.group(1).replace("–", "-") if m else ""


def _parse_event_image(soup: BeautifulSoup) -> Optional[str]:
    """
    Event image՝ նախ og:image, հետո .event_photo img.
    """
    og = soup.select_one("meta[property='og:image']")
    if og and og.get("content"):
        return og["content"].strip()

    img = soup.select_one(".event_photo img")
    if img and img.get("src"):
        src = img["src"].strip()
        return src if src.startswith("http") else BASE_TOMSARKGH_URL + src

    return None


def _parse_event_description(soup: BeautifulSoup) -> str:
    """
    Full Armenian description from .description #eventDesc։
    """
    desc = soup.select_one(".description #eventDesc, .description span#eventDesc")
    if not desc:
        desc = soup.select_one(".description")
    text = desc.decode_contents() if desc else ""
    # մի քիչ մաքրում ենք՝ <br> → newline, strip
    if text:
        text = BeautifulSoup(text, "html.parser").get_text("\n", strip=True)
    return text[:4000]


def scrape_tomsarkgh_event(url: str, category: str) -> bool:
    """
    Scrape SINGLE event page և պահի DB‑ում՝ save_news(...).
    Լցնում ենք՝ title_hy, content_hy, image_url, event_date, event_time, venue_hy, price_hy.
    """
    try:
        logger.info(f"🎫 Scraping event: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # TITLE
        title_el = soup.select_one("h1.event-name") or soup.select_one("h1")
        title_hy = _safe_text(title_el)[:200] or "Միջոցառում"

        # DESCRIPTION
        content_hy = _parse_event_description(soup)

        # DATE/TIME/VENUE/PRICE
        event_date, event_time = _parse_event_datetime(soup)
        venue_hy = _parse_event_venue(soup)
        price_hy = _parse_event_price(soup)

        # IMAGE
        image_url = _parse_event_image(soup)

        # Bilingual: այս պահին EN version-ը չենք քաշում, պահում ենք HY որպես fallback
        title_en = title_hy
        content_en = content_hy

        # SAVE
        save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=category,
            source_url=url,
            event_date=event_date,
            event_time=event_time,
            venue_hy=venue_hy,
            price_hy=price_hy,
        )
        logger.info(
            f"SAVED [{category}] {title_hy[:40]} | 📅{event_date} ⏰{event_time} "
            f"📍{venue_hy[:20]} 💰{price_hy}"
        )
        return True

    except Exception as e:
        logger.error(f"❌ Event error: {url} — {e}")
        return False


# =============================================================================
# MAIN TOMSARKGH SCRAPER — FULL FLOW
# =============================================================================

def scrape_tomsarkgh_events() -> int:
    """
    Main scraper:
    1) անցնում է TOMSARKGH_CATEGORIES mapping‑ի վրա,
    2) յուրաքանչյուր EventType‑ի համար քաշում է list‑ից URL‑ներ,
    3) ամեն URL‑ի համար քաշում է event page և save_news().
    """
    logger.info("▶️ Starting Tomsarkgh scraper (event pages)")
    total_saved = 0

    for event_type, category in TOMSARKGH_CATEGORIES.items():
        logger.info(f"📂 Category={category}, type={event_type}")
        links = fetch_tomsarkgh_events(event_type)

        if not links:
            logger.warning(f"⚠️ No events for type={event_type}")
            continue

        saved_for_type = 0
        for url in links:
            if scrape_tomsarkgh_event(url, category):
                saved_for_type += 1

        logger.info(
            f"✅ {category} (type={event_type}): {saved_for_type}/{len(links)} saved"
        )
        total_saved += saved_for_type

    logger.info(f"✅ === TOMSARKGH SCRAPER COMPLETE: {total_saved} items ===")
    return total_saved


# =============================================================================
# MAIN RUNNER
# =============================================================================

def run_all_scrapers() -> int:
    """
    Run complete news scraping cycle.
    Հիմա ակտիվ է միայն Tomsarkgh; մյուս աղբյուրները (PanARMENIAN, News.am)
    կարող ենք ավելացնել հետո։
    """
    logger.info("🚀 === NEWS SCRAPER START ===")
    total = scrape_tomsarkgh_events()
    logger.info(f"🏁 === NEWS SCRAPER DONE: {total} items ===")
    return total


if __name__ == "__main__":
    run_all_scrapers()
