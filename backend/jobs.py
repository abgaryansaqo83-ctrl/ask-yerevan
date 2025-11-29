# backend/jobs.py

import os
import datetime
from aiogram import Bot

from .armenia.weather import get_yerevan_weather
from .armenia.traffic import get_traffic_status
from .armenia.events import (
    get_week_premiere,
    get_next_day_films_and_plays,
    get_festival_events_7days,
)
from .armenia.news import get_daily_news  # ավելացրինք
from .armenia.recommend import get_recommendations  # ավելացրինք (handler-ի համար)
from .ai.response import generate_morning_tone
from .utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)


def _get_bot() -> Bot:
    """Օգնական՝ ստեղծելու Bot instance-ը մեկ տեղից."""
    return Bot(token=settings.BOT_TOKEN)


def _get_group_chat_id() -> int:
    """Խմբի ID-ն settings-ից / env-ից."""
    return settings.GROUP_CHAT_ID


# ================ 1. Առավոտյան broadcast (ամեն օր 08:00) ===================


async def send_morning_broadcast():
    """
    Ամեն օր 08:00 AskYerevan Morning Broadcast.
    Եղանակ + խցանումներ + AI-generated տեքստ։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        weather = await get_yerevan_weather(settings.OPENWEATHER_API_KEY)
        traffic = await get_traffic_status(settings.GOOGLE_DIRECTIONS_KEY)
        message = await generate_morning_tone(weather, traffic)

        await bot.send_message(chat_id, message)
        logger.info("✅ AskYerevan Morning broadcast sent to group")
    except Exception as e:
        logger.error(f"❌ Morning broadcast failed: {e}")
    finally:
        await bot.session.close()


# ================ 2. Երկուշաբթի՝ շաբաթվա պրեմիերա (08:30) ================


async def send_week_premiere():
    """
    Ամեն երկուշաբթի 08:30.
    Շաբաթվա պրեմիերա (ֆիլմ կամ ներկայացում) — 1 event։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        text = await get_week_premiere()
        await bot.send_message(chat_id, text)
        logger.info("✨ Weekly premiere sent to group")
    except Exception as e:
        logger.error(f"❌ Weekly premiere failed: {e}")
    finally:
        await bot.session.close()


# ================ 3. Երկուշաբթի–ուրբաթ խցանումներ (08:30) ================


async def send_traffic_report():
    """
    Երկուշաբթի–ուրբաթ 08:30 խցանումների հաղորդագրություն.
    Կենտրոն գնացող փողոցներ, որտեղ խցանում կա.
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        text = await get_traffic_status(settings.GOOGLE_DIRECTIONS_KEY)
        await bot.send_message(chat_id, text)
        logger.info("🚗 Traffic report sent to group")
    except Exception as e:
        logger.error(f"❌ Traffic report failed: {e}")
    finally:
        await bot.session.close()


# ================ 4. Չորեքշաբթի–կիրակի՝ հաջորդ օրվա event-ներ (09:00) ================


async def send_next_day_events():
    """
    Չորեքշաբթիից կիրակի, ամեն օր 09:00.
    Հաջորդ օրվա 2 ֆիլմ + 2–3 ներկայացում, առանձին հաղորդագրություններով։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        messages = await get_next_day_films_and_plays(target_date=tomorrow)

        for msg in messages:
            await bot.send_message(chat_id, msg)

        logger.info("🎬 Next day events sent to group")
    except Exception as e:
        logger.error(f"❌ Next day events failed: {e}")
    finally:
        await bot.session.close()


# ================ 5. Չորեքշաբթի՝ փառատոններ (09:30) ===================


async def send_festival_events():
    """
    Չորեքշաբթի օրը 09:30.
    7 օրվա փառատոնային իրադարձություններ (եթե կան).
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        text = await get_festival_events_7days()
        await bot.send_message(chat_id, text)
        logger.info("🎉 Festival events sent to group")
    except Exception as e:
        logger.error(f"❌ Festival events failed: {e}")
    finally:
        await bot.session.close()


# ================ 6. Ամենօրյա news digest (10:00) ===================


async def send_news_digest():
    """
    Ամեն օր 10:00 news digest.
    Երևանի նորություններ + կարևոր իրադարձություններ.
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        text = await get_daily_news()  # news.py-ից
        await bot.send_message(chat_id, text)
        logger.info("📰 News digest sent to group")
    except Exception as e:
        logger.error(f"❌ News digest failed: {e}")
    finally:
        await bot.session.close()


# ================ 7. Recommendation handler (bot.py-ում կօգտագործվի) ===================


async def handle_recommendation_request(query: str, chat_id: int):
    """
    Խմբում recommendation խնդրանքներին պատասխանել.
    Օգտագործվում ա bot.py message handler-ում.
    """
    bot = _get_bot()

    try:
        recommendations = await get_recommendations(query, settings.GOOGLE_MAPS_API_KEY)
        
        for rec in recommendations:
            await bot.send_message(chat_id, rec)
        
        logger.info(f"🍽️ Recommendations sent for query: {query}")
    except Exception as e:
        logger.error(f"❌ Recommendation failed: {e}")
    finally:
        await bot.session.close()
