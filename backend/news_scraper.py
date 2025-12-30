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
            # էստեղ հիմք վերցնենք, թե ոնց ենք փոխում լեզուն
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


        # ---------- SAVE ----------
        save_news(
            title_hy=title_hy,
            title_en=title_en,
            content_hy=content_hy,
            content_en=content_en,
            image_url=image_url,
            category=category,
            source_url=url,
            eventdate=eventdate,
            eventtime=eventtime,
            venue_hy=venue_hy,
            price_hy=price_hy,
        )

        logger.info(
            f"SAVED [{category}] {title_hy[:40]} | 📅{eventdate} ⏰{eventtime} "
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

def scrape_tomsarkgh_events_en_only(urls: list[str]) -> int:
    """Մշակում է միայն EN event URL-ներ՝ լրացնելով title_en/content_en."""
    saved = 0
    for url in urls:
        # category-ը այս պահին կարող ես տալ generic, напр. "events"
        if scrape_tomsarkgh_event(url, category="events"):
            saved += 1
    return saved

# ==========================
#  YEREVAN.AM CITY/IMPORTANT
# ==========================

YEREVAN_NEWS_BASE_HY = "https://www.yerevan.am"
YEREVAN_NEWS_LIST_HY = "https://www.yerevan.am/hy/news/"
YEREVAN_NEWS_LIST_EN = "https://www.yerevan.am/en/news/"

YEREVAN_DAYS_BACK = 15  # վերջին 15 օրվա news
YEREVAN_TIMEOUT = 10


def _parse_yerevan_date(date_text: str) -> datetime | None:
    """
    Օրինակ Ֆորմատներ՝
    18.12.2025
    05.01.2026
    """
    if not date_text:
        return None
    date_text = date_text.strip()
    try:
        return datetime.strptime(date_text, "%d.%m.%Y")
    except Exception:
        logger.warning(f"Yerevan date parse failed for '{date_text}'")
        return None


def _extract_yerevan_list_items(lang: str = "hy") -> list[tuple[str, str, datetime]]:
    """
    Վերադարձնում է list [(detail_url, title, date), ...]
    Միայն վերջին 15 օրվա համար:
    """
    list_url = YEREVAN_NEWS_LIST_HY if lang == "hy" else YEREVAN_NEWS_LIST_EN
    logger.info(f"Yerevan list fetch {lang} -> {list_url}")

    resp = requests.get(list_url, timeout=YEREVAN_TIMEOUT)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    items: list[tuple[str, str, datetime]] = []
    cutoff = datetime.now() - timedelta(days=YEREVAN_DAYS_BACK)

    # layout-ը մոտավորապես՝ div.news-list > article / li
    for block in soup.select(".news-list article, .news-list-item, .news-list li"):
        # detail link
        a = block.select_one("a")
        if not a:
            continue
        href = a.get("href") or ""
        if not href:
            continue
        if not href.startswith("http"):
            href = YEREVAN_NEWS_BASE_HY + href

        # title
        title = (a.get_text(strip=True) or "")[:200]
        if not title:
            continue

        # date
        date_el = (
            block.select_one(".date")
            or block.select_one(".news-date")
            or block.select_one("time")
        )
        date_text = date_el.get_text(strip=True) if date_el else ""
        pub_date = _parse_yerevan_date(date_text)
        if not pub_date:
            continue

        if pub_date < cutoff:
            # Հին է, skip
            continue

        items.append((href, title, pub_date))

    logger.info(f"Yerevan list {lang}: {len(items)} items within last {YEREVAN_DAYS_BACK} days")
    return items


def _fetch_yerevan_detail(url_hy: str, url_en: str | None, category: str) -> bool:
    """
    Քաշում է մեկ news HY/EN, պահում է որպես city/important:
    """
    try:
        # HY էջ
        resp_hy = requests.get(url_hy, timeout=YEREVAN_TIMEOUT)
        resp_hy.raise_for_status()
        soup_hy = BeautifulSoup(resp_hy.text, "html.parser")

        # Վերնագիր HY
        title_el_hy = soup_hy.select_one("h1") or soup_hy.select_one(".news-title")
        title_hy = (title_el_hy.get_text(strip=True) if title_el_hy else "")[:200]

        # Նկար
        image_el = (
            soup_hy.select_one("meta[property='og:image']")
            or soup_hy.select_one(".news-image img")
            or soup_hy.select_one("article img")
        )
        image_url = None
        if image_el:
            image_url = image_el.get("content") or image_el.get("src")
            if image_url and not image_url.startswith("http"):
                image_url = YEREVAN_NEWS_BASE_HY + image_url

        # Բովանդակություն HY
        content_el_hy = (
            soup_hy.select_one(".news-content")
            or soup_hy.select_one("article")
            or soup_hy.select_one(".text")
        )
        content_hy = content_el_hy.get_text("\n", strip=True) if content_el_hy else ""

        # EN էջ (ըստ URL)
        title_en = ""
        content_en = ""
        if url_en:
            try:
                resp_en = requests.get(url_en, timeout=YEREVAN_TIMEOUT)
                resp_en.raise_for_status()
                soup_en = BeautifulSoup(resp_en.text, "html.parser")

                title_el_en = soup_en.select_one("h1") or soup_en.select_one(".news-title")
                title_en = (title_el_en.get_text(strip=True) if title_el_en else "")[:200]

                content_el_en = (
                    soup_en.select_one(".news-content")
                    or soup_en.select_one("article")
                    or soup_en.select_one(".text")
                )
                content_en = content_el_en.get_text("\n", strip=True) if content_el_en else ""
            except Exception as e:
                logger.warning(f"Yerevan EN fetch failed {url_en}: {e}")

        # fallback EN
        if not title_en:
            title_en = title_hy
        if not content_en:
            content_en = content_hy

        savenews(
            titlehy=title_hy,
            titleen=title_en,
            contenthy=content_hy,
            contenten=content_en,
            imageurl=image_url,
            category=category,
            sourceurl=url_hy,
        )
        logger.info(f"Yerevan news saved [{category}] {title_hy[:80]}")
        return True

    except Exception as e:
        logger.error(f"Yerevan detail error {url_hy}: {e}")
        return False


def scrape_yerevan_news():
    """
    Քաշում է վերջին 15 օրվա քաղաքապետարանի news‑երը.
    Հակառակ լեզուները match ենք անում slug‑ով, category֊ն փոխանցվելու է դրսից։
    """
    logger.info("Running Yerevan.am city/important scraper")

    items_hy = _extract_yerevan_list_items(lang="hy")
    items_en = _extract_yerevan_list_items(lang="en")

    # map EN ըստ slug-ի
    en_map: dict[str, str] = {}
    for url_en, _, _ in items_en:
        slug = url_en.rstrip("/").split("/")[-1]
        en_map[slug] = url_en

    saved = 0
    for url_hy, title_hy, pub_date in items_hy:
        slug = url_hy.rstrip("/").split("/")[-1]
        url_en = en_map.get(slug)

        # category logic – ըստ քո ցանկության՝ հիմա default city
        category = "city"

        # Այստեղ կարող ես ավելացնել քո ձեռքով keyword filter,
        # օրինակ "metro", "transport" → important:
        lower = title_hy.lower()
        if any(k in lower for k in ["մետրո", "գազ", "ջուր", "շուրջօրյա", "թիկունք"]):
            category = "important"

        if _fetch_yerevan_detail(url_hy, url_en, category):
            saved += 1

    logger.info(f"Yerevan.am scraper complete: {saved} items saved")
    return saved

# =============================================================================
# MAIN RUNNER
# =============================================================================

def run_all_scrapers() -> int:
    """Run complete news scraping cycle (Tomsarkgh HY + EN-only URLs)."""
    logger.info("🚀 === NEWS SCRAPER START ===")

    # 0) Քաղաքապետարանի city / important news (վերջին 15 օր)
    try:
        total_yerevan = scrape_yerevan_news()
        logger.info(f"🏙️ Yerevan.am news saved: {total_yerevan}")
    except Exception as e:
        logger.error(f"Yerevan.am scraper failed: {e}")
        total_yerevan = 0

    # 1) հիմնական HY scraper (ինչպես նախկինում)
    total_hy = scrape_tomsarkgh_events()

    # 2) հավելյալ EN-only URLs, որոնցով ուզում ես title_en/content_en հաստատ քաշվի
    EN_EVENT_URLS = [
        "https://www.tomsarkgh.am/en/event/50020/%D5%87%D5%B8%D5%B8%D6%82-%D4%B7%D5%A9%D5%A5%D6%80%D5%B6%D5%AB%D5%A1.html",
        "https://www.tomsarkgh.am/en/event/50123/%D4%B2%D6%87%D5%A5%D5%BC%D5%A1%D5%B5%D5%AB%D5%B6-%D5%B3%D5%A5%D5%BA%D5%A8%D5%B6%D5%A9%D5%A1%D6%81.html",
        "https://www.tomsarkgh.am/en/event/50303/Doom-Over.html",
        "https://www.tomsarkgh.am/en/event/50262/%D0%90%D0%BD%D0%B0%D0%BA%D0%BE%D0%BD%D0%B4%D0%B0.html",
        "https://www.tomsarkgh.am/en/event/50179/%D4%B7%D5%AC%D6%86%D5%A5%D6%80%D5%AB-%D5%B6%D5%B8%D6%80-%D5%BF%D5%A1%D6%80%D5%AB%D5%B6.html",
        "https://www.tomsarkgh.am/en/event/44294/%D5%96%D5%B8%D6%80%D5%B7-%D6%87-%D4%B4%D5%A1%D5%BE%D5%AB%D5%A9-%D5%84%D5%B8%D6%82%D5%B7%D5%A5%D5%B2%D5%B5%D5%A1%D5%B6.html",
        "https://www.tomsarkgh.am/en/event/50306/%D0%9A%D0%B2%D0%B8%D0%B7-harry-potter.html",
    ]
    saved_en = scrape_tomsarkgh_events_en_only(EN_EVENT_URLS)
    logger.info(f"✅ EN-only events updated: {saved_en}")

    total = total_yerevan + total_hy + saved_en
    logger.info(f"🏁 === NEWS SCRAPER DONE: {total} items ===")
    return total


if __name__ == "__main__":
    run_all_scrapers()

