# =============================================================================
# backend/news_scraper.py
# =============================================================================

import re
from datetime import date, datetime, timedelta
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from urllib.parse import urljoin

from backend.database import save_news
from backend.utils.logger import logger


def map_tomsarkgh_category(title: str, description: str | None = None) -> str:
    """
    Map Tomsarkgh event to AskYerevan category:
    - culture: theater, cinema, dance, concerts
    - holiday_events: New Year / Christmas / holiday
    - events: everything else
    """
    t = (title or "").lower()
    d = (description or "").lower()
    text = f"{t} {d}"

    # Տարվա տոներ
    holiday_keywords = [
        "new year", "christmas", "xmas",
        "նոր տարի", "ամանոր", "տոնածառ", "սուրբ ծնունդ",
    ]
    if any(k in text for k in holiday_keywords):
        return "holiday_events"

    # Մշակույթ
    culture_keywords = [
        "theatre", "theater", "թատրոն",
        "performance", "opera", "ballet", "պար", "dance",
        "cinema", "film", "movie", "կինո",
        "concert", "համերգ", "symphony", "ensemble",
    ]
    if any(k in text for k in culture_keywords):
        return "culture"

    # Լռությամբ՝ միջոցառումներ
    return "events"
    

def map_tkt_category(section_slug: str, title: str, venue: str | None = None) -> str:
    """
    Map TKT events to AskYerevan categories:
    - culture: theater / opera / ballet
    - events: concerts
    - city: tours, restaurants, clubs, cafes
    """
    s = (section_slug or "").lower()
    t = (title or "").lower()
    v = (venue or "").lower()
    text = " ".join([s, t, v])

    # Մշակույթ
    culture_keywords = [
        "theater", "theatre", "թատրոն",
        "opera", "ballet", "performance",
    ]
    if any(k in text for k in culture_keywords):
        return "culture"

    # Քաղաքային
    city_keywords = [
        "tour", "excursion", "wine country", "wine tour",
        "շրջագայ", "էքսկուրսիա",
        "restaurant", "ռեստորան", "music hall", "cafe",
        "club", "ակումբ", "bar", "բար", "lounge",
        "hard rock cafe", "hard rock", "takri",
    ]
    if any(k in text for k in city_keywords):
        return "city"

    # Միջոցառումներ
    event_keywords = [
        "concert", "համերգ", "festival", "fest", "music", "live",
        "jazz", "rock", "classical", "symphony", "ensemble",
    ]
    if any(k in text for k in event_keywords):
        return "events"

    if "concert" in text or "համերգ" in text:
        return "events"

    return "events"

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
    16: "events",         # Կրկես
    54: "events",         # Stand‑up
    31: "events",         # Ակումբ/փաբ
    21: "events",         # Պար
    6:  "events",         # Կինո
    41: "holiday_events", # Տարվա տոներ (start point)
    1:  "culture",        # Թատրոն
    12: "culture",        # Օպերա‑բալետ
    2:  "culture",        # Կոնցերտ
    10: "culture",        # Պոպ
    7:  "city",           # Քաղաքային
}

def _parse_tkt_image(soup: BeautifulSoup) -> Optional[str]:
    """
    Վերադարձնում է TKT event-ի հիմնական նկարի URL-ը:
    Նախ փորձում է og:image, հետո՝ գլխավոր img:
    """
    # 1) Open Graph og:image
    og = soup.select_one("meta[property='og:image']")
    if og and og.get("content"):
        src = og["content"].strip()
        if src:
            return src

    # 2) Բոլոր img-երից առաջին ոչ-պատահականը (եթե պետք լինի backup)
    img = soup.select_one(".event-poster img, .event_image img, .product_image img, img")
    if img and img.get("src"):
        src = img["src"].strip()
        if src:
            return urljoin("https://www.tkt.am", src)

    return None
    
def scrape_tkt_event_page(url_hy: str, url_en: str | None, section_slug: str) -> bool:
    """
    VERY SIMPLE parser for TKT sample events.
    Հիմա մեզ պետք է վերնագիրը, venue-ը, գինը, որ category mapping-ը ստուգենք.
    """
    try:
        logger.info(f"TKT: scraping {url_hy}")
        resp_hy = requests.get(url_hy, timeout=15, headers=HEADERS)
        resp_hy.raise_for_status()
        soup = BeautifulSoup(resp_hy.text, "html.parser")

        # --- TITLE ---
        title_el = soup.select_one("h1.event-title, h1.product_title, h1")
        title_hy = _safe_text(title_el)[:200]

        if not title_hy:
            alt_title = soup.select_one("h2, .event-title, .product_title")
            title_hy = _safe_text(alt_title)[:200] or "TKT միջոցառում"

        # --- VENUE (ամբողջ հասցե) ---
        venue_block = soup.select_one(
            ".event-location, .event__location, .event-details__place"
        )
        if venue_block:
            venue_hy = _safe_text(venue_block)[:200]
        else:
            # fallback՝ նախորդ line-ով
            full_txt = _full_text(soup)
            venue_hy = ""
            for line in full_txt.splitlines():
                if "Yerevan" in line or "Երևան" in line:
                    venue_hy = line.strip()[:200]
                    break
            if not venue_hy:
                venue_hy = "Երևան"

        # --- PRICE (նվազագույն գին) ---
        full_txt = _full_text(soup)
        nums = re.findall(r"\d[\d\s]{1,}", full_txt)
        prices = []
        for n in nums:
            try:
                val = int(n.replace("\xa0", "").replace(" ", ""))
                if val > 0:
                    prices.append(val)
            except ValueError:
                continue

        price_hy = str(min(prices)) if prices else "0"
        if price_hy in ("0", "00", ""):
            price_hy = "0"

        # --- DATE / TIME ---
        m_dt = re.search(r"(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})", full_txt)
        eventdate = m_dt.group(1) if m_dt else ""
        eventtime = m_dt.group(2) if m_dt else ""

        # --- DESCRIPTION ---
        desc_p = soup.select_one(
            "div.event-description p, .event-description p, "
            ".product_description p, article p"
        )
        content_hy = _safe_text(desc_p)[:800]

        # --- IMAGE ---
        image_url = _parse_tkt_image(soup)

        # --- EN (մինիմալ) ---
        title_en = title_hy
        content_en = content_hy
        if url_en:
            try:
                resp_en = requests.get(url_en, timeout=15, headers=HEADERS)
                resp_en.raise_for_status()
                soup_en = BeautifulSoup(resp_en.text, "html.parser")
                title_en_el = soup_en.select_one(
                    "h1.event-title, h1.product_title, h1"
                )
                t_en = _safe_text(title_en_el)
                if t_en:
                    title_en = t_en[:200]
            except Exception as e:
                logger.warning(f"TKT EN fetch failed {url_en}: {e}")

        category = map_tkt_category(section_slug, title_en, venue_hy)

        save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=category,
            source_url=url_hy,
            eventdate=eventdate,
            eventtime=eventtime,
            venue_hy=venue_hy,
            price_hy=price_hy,
        )
        logger.info(f"TKT SAVED [{category}] {title_hy[:60]}")
        return True

    except Exception as e:
        logger.error(f"TKT error {url_hy}: {e}")
        return False

def scrape_tkt_sample_events() -> int:
    """
    Scrape the 5 hand-picked TKT events you gave (club/theater/concert/tour/restaurant)
    to test mapping.
    """
    events = [
        # club / Hard Rock
        ("https://www.tkt.am/index.php/hy/koncent-pamiati-devida-linca-15-jan-2026/eid/2426",
         "https://www.tkt.am/index.php/en/koncent-pamiati-devida-linca-15-jan-2026/eid/2426",
         "club"),

        # theater
        ("https://www.tkt.am/index.php/hy/k-stanislavsky-theater-smesannye-cuvstva-25-jan-2026/eid/2773",
         "https://www.tkt.am/index.php/en/k-stanislavsky-theater-smesannye-cuvstva-25-jan-2026/eid/2773",
         "theater"),

        # concert
        ("https://www.tkt.am/index.php/hy/antonio-vivaldi-four-seasons-by-mystery-ensemble-30-jan-2026/eid/2563",
         "https://www.tkt.am/index.php/en/antonio-vivaldi-four-seasons-by-mystery-ensemble-30-jan-2026/eid/2563",
         "concert"),

        # tour
        ("https://www.tkt.am/index.php/hy/ararat-khor-virap-noravank-wine-country-31-jan-2026/eid/2607/group/1",
         "https://www.tkt.am/index.php/en/ararat-khor-virap-noravank-wine-country-31-jan-2026/eid/2607/group/1",
         "tour"),

        # restaurant
        ("https://www.tkt.am/index.php/hy/takri-restaurant-and-music-hall-forsh-and-davit-musheghyan-24-jan-2026/eid/2765",
         "https://www.tkt.am/index.php/en/takri-restaurant-and-music-hall-forsh-and-davit-musheghyan-24-jan-2026/eid/2765",
         "restaurant"),
    ]

    saved = 0
    for url_hy, url_en, slug in events:
        if scrape_tkt_event_page(url_hy, url_en, slug):
            saved += 1
    logger.info(f"TKT sample events saved={saved}")
    return saved

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


def scrape_tomsarkgh_event(url: str, category: str) -> bool:
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

        # 🔽 category argument-ը գալիս է TOMSARKGH_CATEGORIES-ից,
        # բայց վերջնականը ճշգրտում ենք ըստ վերնագրի/տեքստի.
        final_category = map_tomsarkgh_category(title_hy, content_hy)

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
    """Run complete news scraping cycle (Tomsarkgh + TKT)."""
    logger.info("🚀 === NEWS SCRAPER START ===")

    # 1) Tomsarkgh
    try:
        total_hy = scrape_tomsarkgh_events()
    except Exception as e:
        logger.error(f"Tomsarkgh scraper failed: {e}")
        total_hy = 0

    # 3) TKT sample events
    try:
        total_tkt = scrape_tkt_sample_events()
        logger.info(f"TKT sample events saved: {total_tkt}")
    except Exception as e:
        logger.error(f"TKT scraper failed: {e}")
        total_tkt = 0

    total = total_hy + total_tkt
    logger.info(f"🏁 === NEWS SCRAPER DONE: {total} items ===")
    return total

if __name__ == "__main__":
    run_all_scrapers()

