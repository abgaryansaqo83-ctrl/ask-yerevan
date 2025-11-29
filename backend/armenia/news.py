# backend/armenia/news.py

import aiohttp
import datetime
from typing import List
from ..utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)

NEWS_SOURCES = {
    "mock": [
        "📰 Երևանի քաղաքապետարանը հայտարարել ա ձմեռային փառատոնի մասին",
        "📢 Նոր բացվել ա սրճարան Komitas 15-ում, բացման ակցիաներ",
        "🎉 Այս հանգստյան «Yerevan Winter Nights» event-ը",
    ]
}


async def get_daily_news() -> str:
    """
    Ամեն օր 10:00 news digest.
    Երևանի կարևոր նորություններ + իրադարձություններ.
    """
    today = datetime.date.today().strftime("%d.%m")
    
    # TODO: հետո կապենք իրական news RSS/API-ներ՝
    # 1. 168.am, news.am, armtimes.com RSS
    # 2. Facebook/Instagram local pages
    # 3. Telegram channels
    
    news_items = NEWS_SOURCES["mock"][:3]  # 3 վերջին նորություն
    
    header = f"📰 AskYerevan News Digest — {today}\n\n"
    
    body = "\n\n".join(news_items)
    
    footer = (
        "\n\n🔎 Ավելի մանրամասն՝ "
        "168.am, news.am, armtimes.com\n"
        "📱 Follow @AskYerevan updates-ների համար"
    )
    
    return header + body + footer


async def get_breaking_news() -> List[str]:
    """
    Urgent/breaking news (եթե կա).
    Օգտագործվում ա bot.py handler-ներում.
    """
    # TODO: իրական breaking news detection
    return ["🚨 Breaking news service coming soon..."]

