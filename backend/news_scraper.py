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
    # 🎉 ՄԻՋՕՑԱՌՈՒՄՆԵՌ (events)
    16: "events",  # Կրկես  
    54: "events",  # Stand-up
    31: "events",  # Ակումբ/փաբ
    21: "events",  # Պար
    6: "events",   # Կինո
    
    # ⛄ ՏՕՆԵՌ (holiday_events)
    41: "holiday_events",
    
    # 🏛️ ՄՇԱԿՈՒՅԹ (culture)
    1: "culture",  # Թատրոն
    12: "culture", # Օպերա-բալետ
    2: "culture",  # Կոնցերտ
    10: "culture", # Պոպ
    
    # 🏙️ ՔԱՂԱՅԻՆ (city)
    7: "city",     # Other events
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
def fetch_tomsarkgh_events(event_type: int, days_ahead: int = 3) -> List[str]:  # 7 → 3
    """Fetch event URLs from Tomsarkgh category page."""
    today = date.today()
    start = today.strftime("%m/%d/%Y")
    end = (today + timedelta(days=days_ahead)).strftime("%m/%d/%Y")  # 7 → 3
    
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
# SINGLE EVENT SCRAPER — BETTER STRUCTURED DATA
# =============================================================================
def scrape_tomsarkgh_event(url: str, category: str) -> bool:
    """ՊԼՈՏ Parser - Christmas Hogwarts example."""
    try:
        logger.info(f"🔗 [{category}] {url}")
        resp = requests.get(url, timeout=15, headers=HEADERS)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # TITLE
        title_hy = _safe_text(soup.select_one("h1")) or "Միջոցառում"
        
        # FULL TEXT (ամբողջը)
        full_text = soup.get_text()
        
        # 📅 DATE - regex patterns
        date_match = re.search(r'(\d{1,2}\.\d{1,2}\.?\d{2,4}|\d{1,2}\s+(?:հունվար|փետրվար|դեկտեմբեր))', full_text)
        event_date = date_match.group(1) if date_match else ""
        
        # 🕐 TIME
        time_match = re.search(r'(\d{1,2}:\d{2})', full_text)
        event_time = time_match.group(1) if time_match else ""
        
        # 📍 VENUE - կոնկրետ patterns
        venue_match = re.search(r'(?:Վայր|Հասցե|Կայարան|Գնացք)[:\s]*([^\n\r]{5,50})', full_text)
        venue_hy = venue_match.group(1).strip()[:50] if venue_match else ""
        
        # 💰 PRICE - կոնկրետ pattern
        price_match = re.search(r'(\d{1,4}(?:,\d{3})?|\d{1,4})\s*(?:դր\.?|դրամ)', full_text)
        price_hy = price_match.group(1).replace(',', '') if price_match else ""
        
        # IMAGE
        image_url = None
        img = soup.select_one("meta[property='og:image']")
        if img:
            image_url = img.get("content")
        
        # SAVE (bilingual fallback)
        save_news(
            title_hy=title_hy[:200],
            title_en=title_hy[:200],
            content_hy=full_text[:500],
            content_en=full_text[:500],
            image_url=image_url,
            category=category,
            source_url=url,
            event_date=event_date,
            event_time=event_time,
            venue_hy=venue_hy,
            price_hy=price_hy,
        )
        
        logger.info(f"✅ {title_hy[:40]} | 📅{event_date} | 🕐{event_time} | 📍{venue_hy} | 💰{price_hy}")
        return True
        
    except Exception as e:
        logger.error(f"❌ {url}: {e}")
        return False

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
# MAIN SCRAPER — SCRAPE ALL CATEGORIES
# =============================================================================
def scrape_tomsarkgh_events():
    """Main scraper: all Tomsarkgh categories."""
    logger.info("🎭 Starting Tomsarkgh scraper...")
    total_saved = 0
    
    for event_type, category in TOMSARKGH_CATEGORIES.items():
        logger.info(f"📋 Category {category} (type {event_type})")
        links = fetch_tomsarkgh_events(event_type)
        
        saved = 0
        for url in links[:5]:  # 5 per category
            if scrape_tomsarkgh_event(url, category):
                saved += 1
        
        total_saved += saved
        logger.info(f"✅ {category}: {saved} saved")
    
    return total_saved
    
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
