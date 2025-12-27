# backend/news_scraper.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

from backend.database import save_news
from backend.utils.logger import logger


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


def scrape_panarmenian_culture():
    """Fetch culture news from PanARMENIAN RSS feeds."""
    for src in PANARMENIAN_RSS_SOURCES:
        url = src["url"]
        lang = src["lang"]
        category_slug = src["category_slug"]

        try:
            logger.info(f"Fetching PanARMENIAN culture RSS: {url}")
            resp = requests.get(url, timeout=10)
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


def scrape_tomsarkgh():
    """Scrape latest events from Tomsarkgh.am"""
    try:
        base_url = "https://www.tomsarkgh.am"
        url = f"{base_url}/hy/news"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find news cards (adjust selectors based on site structure)
        news_items = soup.select(".news-item")[:5]  # Top 5
        
        for item in news_items:
            title_el = item.select_one(".title")
            excerpt_el = item.select_one(".excerpt")
            link_el = item.select_one("a")

            if not title_el or not excerpt_el or not link_el:
                continue

            title_hy = title_el.get_text(strip=True)
            content_hy = excerpt_el.get_text(strip=True)

            href = link_el.get("href", "").strip()
            if not href:
                continue

            # կազմենք լրիվ URL
            if href.startswith("http"):
                event_url = href
            else:
                event_url = base_url + href

            img_el = item.select_one("img")
            image_url = img_el["src"].strip() if img_el and img_el.get("src") else None
            if image_url and image_url.startswith("/"):
                image_url = base_url + image_url

            save_news(
                title_hy=title_hy,
                title_en=title_hy,
                content_hy=content_hy,
                content_en=content_hy,
                image_url=image_url,
                category="events",
                source_url=event_url,
            )
            logger.info(f"Tomsarkgh auto-added news: {title_hy[:80]}")
    
    except Exception as e:
        logger.error(f"Tomsarkgh scraper error: {e}")

def run_all_scrapers():
    """Run all news scrapers"""
    logger.info("Running auto news scrapers...")
    scrape_tomsarkgh()
    scrape_panarmenian_culture()
    logger.info("Auto news scraping complete")
