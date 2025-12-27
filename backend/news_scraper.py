# backend/news_scraper.py

import requests
from bs4 import BeautifulSoup
from backend.database import save_news
from backend.utils.logger import logger

def scrape_tomsarkgh():
    """Scrape latest events from Tomsarkgh.am"""
    try:
        url = "https://www.tomsarkgh.am/hy/news"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find news cards (adjust selectors based on site structure)
        news_items = soup.select('.news-item')[:5]  # Top 5
        
        for item in news_items:
            title_hy = item.select_one('.title').text.strip()
            content_hy = item.select_one('.excerpt').text.strip()
            image_url = item.select_one('img')['src'] if item.select_one('img') else None
            
            # Save to database (English version can be placeholder or auto-translated)
            save_news(
                title_hy=title_hy,
                title_en=title_hy,  # Placeholder
                content_hy=content_hy,
                content_en=content_hy,  # Placeholder
                image_url=image_url
            )
            logger.info(f"Auto-added news: {title_hy[:50]}")
    
    except Exception as e:
        logger.error(f"Tomsarkgh scraper error: {e}")


def run_all_scrapers():
    """Run all news scrapers"""
    logger.info("Running auto news scrapers...")
    scrape_tomsarkgh()
    # Add more scrapers here
    logger.info("Auto news scraping complete")
