# backend/news_scraper.py

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import xml.etree.ElementTree as ET

from backend.database import save_news
from backend.utils.logger import logger

BASE_TOMSARKGH_URL = "https://www.tomsarkgh.am"

# EventType mapping → ինչ category ենք դնում news table-ում
TOMSARKGH_EVENT_TYPES = [
    # Կինո
    {"event_type": 6, "category": "events"},
    # Կրկես
    {"event_type": 16, "category": "events"},
    # Stand-up
    {"event_type": 54, "category": "events"},
    # Ակումբ և փաբ
    {"event_type": 31, "category": "events"},
    # Տարվա տոներ (քն텐츠ի տեսակ՝ հատուկ տոնական)
    {"event_type": 41, "category": "holiday_events"},
]

PANARMENIAN_RSS_SOURCES = [
    {
        "url": "https://stickers.panarmenian.net/feeds/arm/news/culture",
        "lang": "hy",
        "category_slug": "culture",
    },
    {
        "url": "https://stickers.panarmenian.net/feeds/eng/news/culture",
        "lang": "en",
        "category_slug": "culture",
    },
]


def parse_rss_datetime(dt_str: str) -> datetime | None:
    """Parse common RSS datetime formats to datetime or return None."""
    try:
        # Օրինակ: Tue, 24 Dec 2024 15:32:00 +0400
        return datetime.strptime(dt_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception:
        return None


HEADERS = {
    "User-Agent": "AskYerevanBot/1.0 (+https://askyerevan.am)",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
}

def _safe_text(el):
    return el.get_text(strip=True) if el else ""
    
def scrape_panarmenian_culture():
    """Fetch culture news from PanARMENIAN RSS feeds."""
    for src in PANARMENIAN_RSS_SOURCES:
        url = src["url"]
        lang = src["lang"]
        category_slug = src["category_slug"]

        try:
            logger.info(f"Fetching PanARMENIAN culture RSS: {url}")
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()

            root = ET.fromstring(resp.content)

            # RSS structure: <rss><channel><item>...</item></channel></rss>
            for item in root.findall("./channel/item"):
                title = (item.findtext("title") or "").strip()
                description = (item.findtext("description") or "").strip()
                link = (item.findtext("link") or "").strip()
                pub_date_raw = (item.findtext("pubDate") or "").strip()

                published_at = parse_rss_datetime(pub_date_raw)

                if not title or not link:
                    continue

                # Քեզ մոտ DB schema-ից կախված՝ հարմարեցնում ենք դաշտերի map-ը.
                if lang == "hy":
                    title_hy = title
                    title_en = title  # placeholder
                    content_hy = description
                    content_en = description  # placeholder
                else:
                    title_hy = title  # placeholder
                    title_en = title
                    content_hy = description  # placeholder
                    content_en = description

                save_news(
                    title_hy=title_hy,
                    title_en=title_en,
                    content_hy=content_hy,
                    content_en=content_en,
                    image_url=None,
                    category="culture",
                    source_url=link,
                )


                logger.info(f"PanARMENIAN [{lang}] added: {title[:80]}")

        except Exception as e:
            logger.error(f"PanARMENIAN culture scraper error ({url}): {e}")


def scrape_tomsarkgh_event_page(url: str, category: str):
    """
    Մեկ կոնկրետ event-ի էջից քաշում է վերնագիր, նկար, տեքստ
    և պահում news table-ում որպես միջոցառում:
    """
    try:
        logger.info(f"Tomsarkgh event page: {url}")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Tomsarkgh event page error ({url}): {e}")
        return

    soup = BeautifulSoup(resp.text, "html.parser")

    # Վերնագիր — փորձում ենք h1 → page title
    title_el = soup.select_one("h1") or soup.select_one(".event-title")
    title_hy = _safe_text(title_el) or "Միջոցառում"

    # =====================================================
    # ՆՆԴՈՒՆԸ content parsing-ի համար
    # =====================================================
    desc_el = soup.select_one(".event-description") or soup.select_one("article") or soup.select_one(".content")

    # 1. MAIN CONTENT — FIRST 120 chars ONLY (clean snippet)
    content_raw = _safe_text(desc_el)
    snippet_hy = content_raw[:120].rsplit(' ', 1)[0] + "..." if content_raw else ""

    # 2. EXTRACT STRUCTURED INFO
    venue_match = re.search(r'Հասցե[։\:](.*?)(?:\n|$)', content_raw, re.IGNORECASE | re.DOTALL)
    venue_hy = venue_match.group(1).strip()[:80] if venue_match else ""

    price_match = re.search(r'(\d{3,4}[-\d]*)\s*դրամ', content_raw)
    price_hy = price_match.group(1) if price_match else ""

    time_match = re.search(r'(\d{1,2}:\d{2})', content_raw)
    time_hy = time_match.group(1) if time_match else ""

    # 3. FALLBACK content (if no description)
    if not snippet_hy:
        paragraphs = soup.select("p")
        if paragraphs:
            snippet_hy = "\n".join(_safe_text(p) for p in paragraphs[:2])[:120] + "..."

    content_hy = snippet_hy  # short version for cards

    # Նկար — Tomsarkgh event cover (valid CSS selectors)
    img_selectors = [
        "img[src*='/uploads/']",                    # uploads folder
        ".event-image img", ".event-cover img",     # event image classes
        ".event-poster img", ".poster img",         # poster images
        ".main-image img", ".hero-image img",       # hero/main images
        "img[alt*='event']", "img[alt*='poster']",  # event-related alt
        ".content img", "article img"               # content images
    ]

    # Tracking pixel exclude keywords
    exclude_keywords = ["facebook", "google", "pixel", "analytics", "track"]

    img_el = None
    for selector in img_selectors:
        candidates = soup.select(selector)
        for candidate in candidates:
            src = candidate.get("src", "").lower()
            # Tracking pixel չէ
            if any(keyword in src for keyword in exclude_keywords):
                continue
            if src and len(src) > 50:  # reasonable image URL length
                img_el = candidate
                break
        if img_el:
            break

    image_url = img_el.get("src") if img_el else None
    if image_url:
        if image_url.startswith("/"):
            image_url = BASE_TOMSARKGH_URL + image_url
        # Remove tracking parameters if any
        if any(keyword in image_url.lower() for keyword in exclude_keywords):
            image_url = None

    # Պարզ տարբերակ՝ հայերենն ենք լրացնում, անգլերենը նույն տեքստով/կամ placeholder
    title_en = title_hy
    content_en = content_hy

    # Structured data save
    news_data = {
        "title_hy": title_hy[:200],
        "content_hy": content_hy[:500],
        "snippet_hy": snippet_hy[:150],  # NEW
        "venue_hy": venue_hy[:100],      # NEW  
        "price_hy": price_hy[:20],       # NEW
        "image_url": image_url,
        "url": url,
        "source": "tomsarkgh",
        "category": category,
        "pub_date": datetime.now(),
        "pub_date_hy": f"Այսօր"  # կամ date parsing
    }

    news.insert_one(news_data)

    logger.info(f"Tomsarkgh event saved: [{category}] {title_hy[:80]}")


def fetch_tomsarkgh_list(event_type: int, days_ahead: int = 2) -> list[str]:
    """
    Վերադարձնում է տոմսարկղի list էջից event link-երի ցուցակը
    տրված EventType-ի (օր. 6 - կինո, 16 - կրկես, 41 - տոնական):
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
        logger.info(f"Tomsarkgh list: event_type={event_type}, {start} → {end}")
        resp = requests.get(f"{BASE_TOMSARKGH_URL}/list", params=params, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Tomsarkgh list error (event_type={event_type}): {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    links: list[str] = []

    # Event-ի քարտերը սովորաբար լինում են .events-block կամ նման div-երի մեջ
    # Կուզենք վերցնել բոլոր <a href="/hy/event/..."> հղումները
    for a in soup.select("a[href*='/hy/event/']"):
        href = a.get("href", "").strip()
        if not href:
            continue
        if href.startswith("http"):
            full_url = href
        else:
            full_url = BASE_TOMSARKGH_URL + href

        if full_url not in links:
            links.append(full_url)

    logger.info(f"Tomsarkgh list: found {len(links)} events for type={event_type}")
    return links

def scrape_tomsarkgh_events():
    """
    Քաշում է տոմսարկղի մի քանի EventType-երի միջոցառումներ և
    գրանցում news table-ում որպես 'events' կամ 'holiday_events'.
    """
    for cfg in TOMSARKGH_EVENT_TYPES:
        event_type = cfg["event_type"]
        category = cfg["category"]

        links = fetch_tomsarkgh_list(event_type=event_type, days_ahead=2)
        if not links:
            continue

        for url in links:
            scrape_tomsarkgh_event_page(url=url, category=category)


def run_all_scrapers():
    """Run all news scrapers"""
    logger.info("Running auto news scrapers...")

    # Տոմսարկղի միջոցառումներ + տարվա տոներ
    scrape_tomsarkgh_events()

    # Եթե հետո գտնենք PanARMENIAN-ի համար անվտանգ ուղի, սա կբացենք
    # scrape_panarmenian_culture()

    logger.info("Auto news scraping complete")
