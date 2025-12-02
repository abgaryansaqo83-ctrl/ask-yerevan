# backend/jobs.py

from aiogram import Bot
from config.settings import settings
from backend.utils.logger import logger
from .armenia.traffic import get_traffic_status
from .armenia.weather import get_yerevan_weather

def _get_bot() -> Bot:
    """Օգնական՝ ստեղծելու Bot instance-ը մեկ տեղից."""
    return Bot(token=settings.BOT_TOKEN)

def _get_group_chat_id() -> int:
    """Խմբի ID-ն settings-ից / env-ից."""
    return settings.GROUP_CHAT_ID

async def send_morning_broadcast():
    """
    Ամեն օր 08:00՝ Երևանի եղանակի հաղորդագրություն։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        weather = await get_yerevan_weather(settings.OPENWEATHER_API_KEY)
        await bot.send_message(chat_id, weather)
        logger.info("✅ Morning weather sent to group")
    except Exception as e:
        logger.error(f"❌ Morning weather failed: {e}")
    finally:
        await bot.session.close()

async def send_traffic_report():
    """
    Երկուշաբթի–ուրբաթ 08:30՝ ճանապարհների խցանման հաղորդագրություն
    (իմացությամբ՝ հիմնական փողոցներում դեպի կենտրոն)
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

# ================ 2. Երկուշաբթի՝ շաբաթվա պրեմիերա (08:30) ================

async def send_week_premiere():
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


# ================ 3. Չորեքշաբթի–կիրակի՝ հաջորդ օրվա event-ներ (09:00) ================

async def send_next_day_events():
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


# ================ 4. Չորեքշաբթի՝ փառատոններ (09:30) ===================

async def send_festival_events():
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


# ================ 6. Recommendation handler (bot.py-ում) ===================

async def handle_recommendation_request(query: str, chat_id: int):
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
