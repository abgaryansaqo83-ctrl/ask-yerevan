# backend/news_scraper.py - COMPLETE BILINGUAL VERSION

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import xml.etree.ElementTree as ET

from backend.database import save_news
from backend.utils.logger import logger

BASE_TOMSARKGH_URL = "https://www.tomsarkgh.am"

# =============================================================================
# EVENT TYPE MAPPING
# =============================================================================
TOMSARKGH_EVENT_TYPES = [
    # Կինո
    {"event_type": 6, "category": "events"},
    # Կրկես
    {"event_type": 16, "category": "events"},
    # Stand-up
    {"event_type": 54, "category": "events"},
    # Ակումբ և փաբ
    {"event_type": 31, "category": "events"},
    # Տարվա տոներ
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

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def parse_rss_datetime(dt_str: str) -> datetime | None:
    """Parse common RSS datetime formats to datetime or return None."""
    try:
        return datetime.strptime(dt_str, "%a, %d %b %Y %H:%M:%S %z")
    except Exception:
        return None

def _safe_text(el):
    return el.get_text(strip=True) if el else ""

HEADERS = {
    "User-Agent": "AskYerevanBot/1.0 (+https://askyerevan.am)",
    "Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8",
}

# =============================================================================
# PANARMENIAN RSS SCRAPER (DISABLED - READY)
# =============================================================================
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
            for item in root.findall("./channel/item"):
                title = (item.findtext("title") or "").strip()
                description = (item.findtext("description") or "").strip()
                link = (item.findtext("link") or "").strip()
                pub_date_raw = (item.findtext("pubDate") or "").strip()

                if not title or not link:
                    continue

                if lang == "hy":
                    title_hy, title_en = title, title  # placeholder
                    content_hy, content_en = description, description
                else:
                    title_hy, title_en = title, title
                    content_hy, content_en = description, description

                save_news(
                    title_hy=title_hy,
                    title_en=title_en,
                    content_hy=content_hy,
                    content_en=content_en,
                    image_url=None,
                    category=category_slug,
                    source_url=link,
                )
                logger.info(f"PanARMENIAN [{lang}] added: {title[:80]}")

        except Exception as e:
            logger.error(f"PanARMENIAN culture scraper error ({url}): {e}")

# =============================================================================
# TOMSARKGH BILINGUAL EVENT SCRAPER (MAIN)
# =============================================================================
def scrape_tomsarkgh_event_page(url: str, category: str):
    """
    Bilingual Tomsarkgh event scraper:
    - Scrapes HY + EN versions automatically
    - Extracts venue, price, snippet
    - Perfect for hy/en toggle sites
    """
    try:
        logger.info(f"Tomsarkgh event page: {url}")
        
        # =====================================================
        # 1. BILINGUAL PARSING (HY + EN)
        # =====================================================
        # Armenian version (default)
        resp_hy = requests.get(url, timeout=15)
        resp_hy.raise_for_status()
        soup_hy = BeautifulSoup(resp_hy.text, "html.parser")
        
        title_hy = _safe_text(soup_hy.select_one("h1")) or "Միջոցառում"
        desc_hy = soup_hy.select_one(".description, .event_resume, article, .content")
        content_hy_raw = _safe_text(desc_hy)
        
        # English version (lang=en toggle)
        url_en = url.replace("/hy/event/", "/en/event/")
        title_en = title_hy  # fallback
        content_en_raw = content_hy_raw
        
        try:
            resp_en = requests.get(url_en, timeout=10)
            resp_en.raise_for_status()
            soup_en = BeautifulSoup(resp_en.text, "html.parser")
            title_en = _safe_text(soup_en.select_one("h1")) or title_hy
            desc_en = soup_en.select_one(".description, .event_resume, article, .content")
            content_en_raw = _safe_text(desc_en) or content_hy_raw
        except Exception as e:
            logger.debug(f"EN version fallback: {e}")
        
        # =====================================================
        # 2. STRUCTURED EXTRACTION (venue, price, snippet)
        # =====================================================
        snippet_hy = content_hy_raw[:120].rsplit(' ', 1)[0] + "..." if content_hy_raw else ""
        
        # Venue (Հասցե կամ Կազմակերպիչ)
        venue_match = re.search(r'(Հասցե|Կազմակերպիչ|Venue)[։\:](.*?)(?:\n|$)', content_hy_raw, re.IGNORECASE | re.DOTALL)
        venue_hy = venue_match.group(2).strip()[:80] if venue_match else ""
        
        # Price
        price_match = re.search(r'(\d{3,4}[-\d]*)\s*(?:դրամ|AMD)', content_hy_raw)
        price_hy = price_match.group(1) if price_match else ""
        
        content_hy = content_hy_raw[:500]
        content_en = content_en_raw[:500]
        
        # =====================================================
        # 3. IMAGE EXTRACTION
        # =====================================================
        img_el = None
        img_selectors = [
            "img[src*='/thumbnails/']",  # priority
            "img[src*='/uploads/']", 
            ".event_photo img",
            ".hero img, .poster img",
            "meta[property='og:image']",
        ]
        
        for selector in img_selectors:
            candidates = soup_hy.select(selector)
            for candidate in candidates[:3]:
                src = candidate.get("src") or candidate.get("content")
                if src and len(src) > 30 and "facebook" not in src.lower():
                    img_el = candidate
                    break
            if img_el:
                break
                
        image_url = img_el.get("src") or img_el.get("content") if img_el else None
        if image_url and image_url.startswith("/"):
            image_url = "https://www.tomsarkgh.am" + image_url

        # =====================================================
        # 4. POSTGRESQL SAVE (BILINGUAL)
        # =====================================================
        from backend.database import get_connection
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO news (title_hy, title_en, content_hy, content_en, snippet_hy, 
                              venue_hy, price_hy, image_url, source_url, category)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            title_hy[:200],
            title_en[:200],
            content_hy[:500],
            content_en[:500],
            snippet_hy[:150],
            venue_hy[:100],
            price_hy[:20],
            image_url,
            url,
            category
        ))
        
        conn.commit()
        conn.close()
        logger.info(f"✅ [{category}] {title_hy[:40]} | 🇭🇺{title_en[:30]} | 📍{venue_hy[:20]} | 💰{price_hy}")
        
    except Exception as e:
        logger.error(f"Tomsarkgh event page error ({url}): {e}")

# =============================================================================
# TOMSARKGH LIST FETCHER
# =============================================================================
def fetch_tomsarkgh_list(event_type: int, days_ahead: int = 2) -> list[str]:
    """Fetch event links from Tomsarkgh list page."""
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

# =============================================================================
# MAIN TOMSARKGH SCRAPER
# =============================================================================
def scrape_tomsarkgh_events():
    """Scrape multiple Tomsarkgh event types."""
    for cfg in TOMSARKGH_EVENT_TYPES:
        event_type = cfg["event_type"]
        category = cfg["category"]

        links = fetch_tomsarkgh_list(event_type=event_type, days_ahead=2)
        if not links:
            continue

        for url in links[:5]:  # limit per category
            scrape_tomsarkgh_event_page(url=url, category=category)

# =============================================================================
# MAIN RUNNER
# =============================================================================
def run_all_scrapers():
    """Run all news scrapers"""
    logger.info("🚀 Running auto news scrapers...")

    # Tomsarkgh events + holidays (MAIN)
    scrape_tomsarkgh_events()

    # PanARMENIAN culture (future)
    # scrape_panarmenian_culture()

    logger.info("✅ Auto news scraping complete")

if __name__ == "__main__":
    run_all_scrapers()
