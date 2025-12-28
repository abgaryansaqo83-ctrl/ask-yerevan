# =============================================================================
# backend/news_scraper.py — TOMSARKGH BILINGUAL SCRAPER
# =============================================================================
# Scrape events from tomsarkgh.am with proper categories for submenu
# Categories: culture, events, city, important, holiday_events
# =============================================================================

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional
from backend.database import save_news
from backend.utils.logger import logger

BASE_TOMSARKGH_URL = "https://www.tomsarkgh.am"
HEADERS = {
    "User-Agent": "AskYerevanBot/1.0 (+https://askyerevan.am)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# =============================================================================
# EVENT TYPE MAPPING (Tomsarkgh → Our Categories)
# =============================================================================
TOMSARKGH_CATEGORIES = {
    # 🎉 Միջոցառումներ (events)
    6: "events",   # Կինո / Cinema
    16: "events",  # Կրկես / Circus  
    54: "events",  # Stand-up
    31: "events",  # Ակումբ/փաբ / Clubs & Pubs
    
    # ⛄ Տարվա տոներ (holiday_events)
    41: "holiday_events",
    
    # 🏛️ Մշակույթ (culture)
    1: "culture",  # Թատրոն / Theater
    2: "culture",  # Կոնցերտ / Concert
    12: "culture", # Օպերա-բալետ / Opera-Ballet
    
    # 🏙️ Քաղաքային (city) - քաղաքի իրադարձություններ
    7: "city",     # Other events
    
    # ⚠️ Կարևոր (important) - հատուկ իրադարձություններ
    55: "important", # Special events
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
def _safe_text(el) -> str:
    """Extract clean text from BeautifulSoup element."""
    return el.get_text(strip=True) if el else ""

def parse_venue(text: str) -> str:
    """Extract venue from event text."""
    patterns = [
        r'(Հասցե|Վայր|Թատրոն|Կինո|Venue|Place)[:։]\s*(.*?)(?:\n|$)',
        r'(\w+\s+(?:թատրոն|կինո|սրահ|hall|cinema))',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()[:100]
    return ""

def parse_price(text: str) -> str:
    """Extract price from event text."""
    match = re.search(r'(\d{3,})[.,]?\d*\s*(?:դր\.?|AMD|դրամ)', text)
    return match.group(1) if match else ""

# =============================================================================
# TOMSARKGH LIST FETCHER
# =============================================================================
def fetch_tomsarkgh_events(event_type: int, days_ahead: int = 7) -> List[str]:
    """Fetch event URLs from Tomsarkgh category page."""
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
        resp = requests.get(f"{BASE_TOMSARKGH_URL}/list", params=params, timeout=15, headers=HEADERS)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"❌ Tomsarkgh list error (type={event_type}): {e}")
        return []
    
    soup = BeautifulSoup(resp.text, "html.parser")
    links = []
    
    # Extract event links
    for a in soup.select("a[href*='/hy/event/']"):
        href = a.get("href", "").strip()
        if href and '/hy/event/' in href:
            full_url = href if href.startswith('http') else BASE_TOMSARKGH_URL + href
            if full_url not in links:
                links.append(full_url)
    
    logger.info(f"✅ Found {len(links)} events for type={event_type}")
    return links[:10]  # Limit per category

# =============================================================================
# SINGLE EVENT SCRAPER
# =============================================================================
def scrape_tomsarkgh_event(url: str, category: str) -> bool:
    """Scrape single event page with bilingual support."""
    try:
        logger.info(f"🔗 Scraping: {url}")
        
        # Armenian version (main)
        resp_hy = requests.get(url, timeout=15, headers=HEADERS)
        resp_hy.raise_for_status()
        soup_hy = BeautifulSoup(resp_hy.text, "html.parser")
        
        # Extract Armenian content
        title_hy = _safe_text(soup_hy.select_one("h1")) or "Միջոցառում"
        desc_hy = soup_hy.select_one(".description, .event_resume, .content, article p")
        content_hy = _safe_text(desc_hy)[:800] or "Մանրամասները կայքում:"
        
        # Extract structured data
        venue_hy = parse_venue(content_hy)
        price_hy = parse_price(content_hy)
        
        # Try English version (optional)
        title_en = title_hy  # fallback
        content_en = content_hy
        try:
            url_en = url.replace("/hy/event/", "/en/event/")
            resp_en = requests.get(url_en, timeout=10, headers=HEADERS)
            soup_en = BeautifulSoup(resp_en.text, "html.parser")
            title_en = _safe_text(soup_en.select_one("h1")) or title_hy
            content_en = _safe_text(soup_en.select_one(".description, .content"))[:800]
        except:
            logger.debug(f"EN version unavailable: {url_en}")
        
        # Extract image
        img_selectors = [
            "meta[property='og:image']",
            "img[src*='thumbnails']", 
            ".event-image img",
            ".main-image img"
        ]
        image_url = None
        for selector in img_selectors:
            img = soup_hy.select_one(selector)
            if img:
                image_url = img.get("content") or img.get("src")
                if image_url and not image_url.startswith("http"):
                    image_url = BASE_TOMSARKGH_URL + image_url
                break
        
        # Save to database (upsert)
        save_news(
            title_hy=title_hy.strip()[:200],
            title_en=title_en.strip()[:200],
            content_hy=content_hy.strip(),
            content_en=content_en.strip(),
            image_url=image_url,
            category=category,
            source_url=url,
        )
        
        logger.info(f"✅ SAVED [{category}] {title_hy[:50]}... | 📍{venue_hy[:20]}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Event error ({url}): {e}")
        return False

# =============================================================================
# MAIN SCRAPER — SCRAPE ALL CATEGORIES
# =============================================================================
def scrape_tomsarkgh_events():
    """Main scraper: all Tomsarkgh categories for our submenu."""
    logger.info("🎭 Starting Tomsarkgh bilingual scraper...")
    
    total_saved = 0
    for event_type, category in TOMSARKGH_CATEGORIES.items():
        logger.info(f"--- Category: {category} (type {event_type}) ---")
        
        # Get event list
        links = fetch_tomsarkgh_events(event_type)
        if not links:
            logger.warning(f"No events for {category}")
            continue
        
        # Scrape each event (limit 8 per category)
        saved_count = 0
        for url in links[:8]:
            if scrape_tomsarkgh_event(url, category):
                saved_count += 1
        
        total_saved += saved_count
        logger.info(f"✅ {category}: {saved_count}/{len(links)} saved")
    
    logger.info(f"🎉 TOTAL: {total_saved} events scraped!")
    return total_saved

# =============================================================================
# PANARMENIAN RSS (Culture only - optional)
# =============================================================================
def scrape_panarmenian_culture():
    """Scrape culture news from PanARMENIAN RSS (DISABLED by default)."""
    rss_feeds = [
        "https://stickers.panarmenian.net/feeds/arm/news/culture",
        "https://stickers.panarmenian.net/feeds/eng/news/culture",
    ]
    
    for url in rss_feeds:
        try:
            resp = requests.get(url, timeout=15, headers=HEADERS)
            root = ET.fromstring(resp.content)
            
            for item in root.findall(".//item")[:5]:  # Limit 5 per feed
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                desc = item.findtext("description", "").strip()
                
                if title and link:
                    save_news(
                        title_hy=title, title_en=title,
                        content_hy=desc[:500], content_en=desc[:500],
                        category="culture",
                        source_url=link,
                    )
                    logger.info(f"📖 PanARMENIAN culture: {title[:60]}")
        except Exception as e:
            logger.error(f"PanARMENIAN error: {e}")

# =============================================================================
# MAIN RUNNER
# =============================================================================
def run_all_scrapers():
    """Run complete news scraping cycle."""
    logger.info("🚀 === NEWS SCRAPER START ===")
    
    # Main: Tomsarkgh events (all categories)
    total = scrape_tomsarkgh_events()
    
    # Optional: PanARMENIAN culture RSS
    # scrape_panarmenian_culture()
    
    logger.info(f"✅ === SCRAPER COMPLETE: {total} items ===")
    return total

if __name__ == "__main__":
    run_all_scrapers()
