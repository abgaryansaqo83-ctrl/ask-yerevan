# =============================================================================
# backend/news_scraper.py
# =============================================================================

import re
from datetime import date, timedelta
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from backend.database import save_news
from backend.utils.logger import logger


# =============================================================================
# CATEGORY LOGIC
# =============================================================================

def map_tomsarkgh_category(title: str, description: str | None = None) -> str:
    """
    Keyword-based guess for Tomsarkgh events:
    - holiday_events: Նոր տարի / Christmas / տոնածառ և այլն
    - culture: theatre, cinema, opera, ballet, dance, etc.
    - city: some explicitly city‑related things
    - events: everything else
    """
    t = (title or "").lower()
    d = (description or "").lower()
    text = f"{t} {d}"

    # --- Holiday / seasonal ---
    holiday_keywords = [
        "new year", "new-year", "new year’s", "new years",
        "christmas", "xmas",
        "նոր տարի", "ամանոր", "տոնածառ", "սուրբ ծնունդ",
        "christmas market", "christmas fair",
    ]
    if any(k in text for k in holiday_keywords):
        return "holiday_events"

    # --- Culture (art) ---
    culture_keywords = [
        # theatre / performance
        "theatre", "theater", "թատրոն", "performance",
        "play", "dramatic", "drama",
        # opera / ballet / dance
        "opera", "օպերա", "ballet", "բալետ",
        "dance show", "dance performance", "պարային",
        # cinema / films
        "cinema", "film", "movie", "screening", "premiere", "կինո",
        # music / concerts of artistic type
        "symphony", "orchestra", "ensemble", "quartet", "choir",
        "classical music", "chamber music",
    ]
    if any(k in text for k in culture_keywords):
        return "culture"

    # --- Explicitly city-related ---
    city_keywords = [
        "city day", "քաղաքի տոն",
        "city tour", "քաղաքային զբոսանք",
        "քաղաքապետարան", "city hall",
    ]
    if any(k in text for k in city_keywords):
        return "city"

    # Default guess
    return "events"


def final_category_from_source(
    base_category: str, title: str, description: str | None
) -> str:
    """
    Combine EventType‑ից եկած base_category + keyword‑based guessed category.

    Ցանկությունդ էր՝
    - 41 / seasonal → holiday_events
    - 1,6,12,21 → culture միայն արվեստի համար
    - 7 → city
    - 16,31,54,10,2 և մնացածը → events (generic միջոցառումներ)
    """
    guessed = map_tomsarkgh_category(title, description)

    # 1) Seasonal միշտ holiday_events
    if base_category == "holiday_events" or guessed == "holiday_events":
        return "holiday_events"

    # 2) Մաքուր արվեստի EventType-եր՝ միշտ culture
    if base_category == "culture":
        return "culture"

    # 3) Քաղաքային
    if base_category == "city":
        return "city"

    # 4) Մնացածը՝ events (կրկես, stand-up, club, pop, concerts, uncategorized)
    return "events"


# =============================================================================
# CONSTANTS
# =============================================================================

BASE_TOMSARKGH_URL = "https://www.tomsarkgh.am"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Tomsarkgh EventType IDs → base AskYerevan categories
# Հստակ դասավորությունդ.
TOMSARKGH_CATEGORIES = {
    16: "events",         # Կրկես
    54: "events",         # Stand‑up
    31: "events",         # Ակումբ/փաբ
    10: "events",         # Պոպ
    2:  "events",         # Կոնցերտ
    41: "holiday_events", # Տարվա տոներ (seasonal only)
    1:  "culture",        # Թատրոն
    6:  "culture",        # Կինո
    12: "culture",        # Օպերա‑բալետ
    21: "culture",        # Պար
    7:  "city",           # Քաղաքային
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

    for a in soup.select("a[href*='/hy/event/']"):
        href = a.get("href", "").strip()
        if not href or "/hy/event/" not in href:
            continue
        full_url = href if href.startswith("http") else BASE_TOMSARKGH_URL + href
        if full_url not in links:
            links.append(full_url)

    logger.info(f"✅ Found {len(links)} events for type={event_type}")
    return links[:20]


# =============================================================================
# EVENT PAGE PARSER
# =============================================================================

def _parse_event_datetime(soup: BeautifulSoup) -> (str, str):
    """
    Return (eventdate, eventtime) strings.
    """
    meta = soup.select_one("meta[itemprop='startDate']")
    eventdate = ""
    eventtime = ""

    if meta and meta.get("content"):
        raw = meta["content"].strip()  # "2025-12-30 14:00"
        parts = raw.split()
        if len(parts) >= 1:
            eventdate = parts[0]
        if len(parts) >= 2:
            eventtime = parts[1]

    txt = _full_text(soup)
    if not eventdate:
        m = re.search(r"(\d{4}-\d{2}-\d{2})", txt)
        if m:
            eventdate = m.group(1)
    if not eventtime:
        m = re.search(r"(\d{1,2}[:․]\d{2})", txt)
        if m:
            eventtime = m.group(1).replace("․", ":")

    return eventdate[:32], eventtime[:32]


def _parse_event_venue(soup: BeautifulSoup) -> str:
    el = soup.select_one(".occurrence_venue span[itemprop='name']")
    if el:
        return _safe_text(el)[:100]

    txt = _full_text(soup)
    m = re.search(
        r"(թատրոն|ակումբ|ջազ ակումբ|համերգասրահ|cinema|hall)[^\n]{0,80}",
        txt,
        re.IGNORECASE,
    )
    return m.group(0).strip()[:100] if m else ""


def _parse_event_price(soup: BeautifulSoup) -> str:
    meta_price = soup.select_one(
        "span[itemprop='offers'] meta[itemprop='price'], meta[itemprop='price']"
    )
    if meta_price and meta_price.get("content"):
        raw = meta_price["content"].strip()
        m = re.match(r"(\d+)", raw)
        if m:
            return m.group(1)

    txt = _full_text(soup)
    m = re.search(r"(\d{3,}(?:[-–]\d{3,})?)\s*(?:դր\.?|դրամ|AMD)", txt)
    return m.group(1).replace("–", "-") if m else ""


def _parse_event_image(soup: BeautifulSoup) -> Optional[str]:
    og = soup.select_one("meta[property='og:image']")
    if og and og.get("content"):
        return og["content"].strip()

    img = soup.select_one(".event_photo img")
    if img and img.get("src"):
        src = img["src"].strip()
        return src if src.startswith("http") else BASE_TOMSARKGH_URL + src

    return None


def _parse_event_description(soup: BeautifulSoup) -> str:
    desc = soup.select_one(".description #eventDesc, .description span#eventDesc")
    if not desc:
        desc = soup.select_one(".description")
    text = desc.decode_contents() if desc else ""
    if text:
        text = BeautifulSoup(text, "html.parser").get_text("\n", strip=True)
    return text[:4000]


def scrape_tomsarkgh_event(
    url: str,
    base_category: str,
    event_type: Optional[int] = None,
) -> bool:
    """Scrape single event page (HY + optional EN) and save to DB."""
    try:
        logger.info(f"🎫 Scraping event: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # ---------- HY VERSION ----------
        title_el = soup.select_one("h1.event-name") or soup.select_one("h1")
        title_hy = _safe_text(title_el)[:200] or "Միջոցառում"

        content_hy = _parse_event_description(soup)
        eventdate, eventtime = _parse_event_datetime(soup)
        venue_hy = _parse_event_venue(soup)
        price_hy = _parse_event_price(soup)
        image_url = _parse_event_image(soup)

        # ---------- EN VERSION (optional) ----------
        title_en = title_hy
        content_en = content_hy

        try:
            if "/hy/event" in url:
                url_en = url.replace("/hy/event", "/en/event")
            elif "/en/event" in url:
                url_en = url
            else:
                url_en = url.replace("/hy/", "/en/")

            resp_en = requests.get(url_en, headers=HEADERS, timeout=10)
            resp_en.raise_for_status()
            soup_en = BeautifulSoup(resp_en.text, "html.parser")

            title_en_el = soup_en.select_one("h1.event-name") or soup_en.select_one("h1")
            en_title = _safe_text(title_en_el)
            if en_title:
                title_en = en_title[:200]

            desc_en = soup_en.select_one(".description #eventDesc, .description, article, .content")
            if desc_en:
                text_en = BeautifulSoup(
                    desc_en.decode_contents(), "html.parser"
                ).get_text("\n", strip=True)
                if text_en:
                    content_en = text_en[:4000]
        except Exception:
            logger.debug(f"EN version unavailable for {url}")

        # ---------- CATEGORY FINAL ----------
        final_category = final_category_from_source(base_category, title_hy, content_hy)

        # ---------- SAVE ----------
        save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=final_category,
            source_url=url,
            eventdate=eventdate,
            eventtime=eventtime,
            venue_hy=venue_hy,
            price_hy=price_hy,
        )

        logger.info(
            f"SAVED [{final_category}] {title_hy[:40]} | 📅{eventdate} ⏰{eventtime} "
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
    """Scrape all mapped Tomsarkgh categories."""
    logger.info("▶️ Starting Tomsarkgh scraper (event pages)")
    total_saved = 0

    for event_type, base_category in TOMSARKGH_CATEGORIES.items():
        logger.info(f"📂 Category={base_category}, type={event_type}")
        links = fetch_tomsarkgh_events(event_type)

        if not links:
            logger.warning(f"⚠️ No events for type={event_type}")
            continue

        saved_for_type = 0
        for url in links:
            if scrape_tomsarkgh_event(url, base_category, event_type=event_type):
                saved_for_type += 1

        logger.info(
            f"✅ {base_category} (type={event_type}): {saved_for_type}/{len(links)} saved"
        )
        total_saved += saved_for_type

    logger.info(f"✅ === TOMSARKGH SCRAPER COMPLETE: {total_saved} items ===")
    return total_saved


# =============================================================================
# MAIN RUNNER
# =============================================================================

def run_all_scrapers() -> int:
    """Run complete news scraping cycle (Tomsarkgh + PanARMENIAN)."""
    logger.info("🚀 === NEWS SCRAPER START ===")

    total = 0

    # 1) Tomsarkgh
    try:
        total_hy = scrape_tomsarkgh_events()
        total += total_hy
    except Exception as e:
        logger.error(f"Tomsarkgh scraper failed: {e}")

    logger.info(f"🏁 === NEWS SCRAPER DONE: {total} items ===")
    return total


if __name__ == "__main__":
    run_all_scrapers()
