# backend/jobs.py

import os
import datetime
from aiogram import Bot

from .armenia.weather import get_yerevan_weather
from .armenia.traffic import get_traffic_status
from .armenia.events import (
    get_week_premiere,
    get_next_day_films_and_plays,
)
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


# ================ 1. Առավոտյան broadcast ===================


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


# ================ 2. Երկուշաբթի՝ շաբաթվա պրեմիերա ================


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


# ================ 3. Չորեքշաբթի–կիրակի՝ հաջորդ օրվա event-ներ ================


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


# ================ 4. News digest (placeholder) ===================


async def send_news_digest():
    """
    Placeholder: News digest / փառատոնային շաբաթ և այլն.
    Հետագայում կկապենք events + news աղբյուրներին։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        text = (
            "📰 AskYerevan news digest-ը դեռ պատրաստման փուլում է.\n"
            "Շուտով այստեղ կլինեն Երևանի ամենօրյա նորությունները և իրադարձությունները։"
        )
        await bot.send_message(chat_id, text)
        logger.info("ℹ️ News digest stub sent")
    except Exception as e:
        logger.error(f"❌ News digest failed: {e}")
    finally:
        await bot.session.close()
