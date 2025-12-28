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
    try:
        logger.info(f"Tomsarkgh event page: {url}")
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Վերնագիր
        title_el = soup.select_one("h1") or soup.select_one(".event-title")
        title_hy = _safe_text(title_el) or "Միջոցառում"

        # Content parsing (ՆՈՐ)
        desc_el = soup.select_one(".event-description") or soup.select_one("article") or soup.select_one(".content")
        content_raw = _safe_text(desc_el)
        snippet_hy = content_raw[:120].rsplit(' ', 1)[0] + "..." if content_raw else ""
        
        venue_match = re.search(r'Հասցե[։\:](.*?)(?:\n|$)', content_raw, re.IGNORECASE | re.DOTALL)
        venue_hy = venue_match.group(1).strip()[:80] if venue_match else ""
        price_match = re.search(r'(\d{3,4}[-\d]*)\s*դրամ', content_raw)
        price_hy = price_match.group(1) if price_match else ""
        
        content_hy = snippet_hy

        # Նկար (նույնը մնում ա)
        img_el = None
        img_selectors = ["img[src*='/uploads/']", ".hero img", ".poster img"]
        for selector in img_selectors:
            candidates = soup.select(selector)
            for candidate in candidates:
                src = candidate.get("src", "").lower()
                if src and len(src) > 30:
                    img_el = candidate
                    break
            if img_el:
                break
        image_url = img_el.get("src") if img_el else None
        if image_url and image_url.startswith("/"):
            image_url = "https://www.tomsarkgh.am" + image_url

        # SQLITE SAVE (ՆՈՐ)
        from backend.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO news (title_hy, content_hy, snippet_hy, venue_hy, price_hy, 
                            image_url, url, source, category, pub_date_hy, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NOW())
            ON CONFLICT (url) DO NOTHING
        """, (
            title_hy[:200],
            content_hy[:500],
            snippet_hy[:150],
            venue_hy[:100],
            price_hy[:20],
            image_url,
            url,
            "tomsarkgh",
            category,
            "Այսօր"
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Saved: {title_hy[:50]} | 📍{venue_hy} | 💰{price_hy}")
        
    except Exception as e:
        logger.error(f"Tomsarkgh event page error ({url}): {e}")


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
