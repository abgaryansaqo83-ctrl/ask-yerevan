# backend/jobs.py

import datetime

from aiogram import Bot

from backend.config.settings import settings
from backend.utils.logger import logger
from backend.database import get_events_for_date
from backend.armenia.traffic import get_traffic_status
from backend.armenia.weather import get_yerevan_weather
from backend.armenia.recommend import get_recommendations
from backend.database import get_unanswered_questions_older_than, mark_question_answered
from backend.ai.response import generate_reply

BASE_URL = "https://askyerevan.am"


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

# ================ 2. Երկուշաբթի՝ տարվա տոները (08:30) ================

async def send_holiday_events():
    """
    Երկուշաբթի 08:30 — ուղարկում է մոտակա holiday_events-ի event-ները
    (օրինակ՝ Ամանոր, Սուրբ Ծնունդ, Մարտի 8 և այլն), DB-ից։
    Յուրաքանչյուր event առանձին մեսիջով, քարտանման caption-ով։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        rows = get_upcoming_holiday_events(days_ahead=14, limit=10)

        if not rows:
            logger.info("ℹ️ No upcoming holiday events found")
            await bot.send_message(chat_id, "Տարվա տոների հատուկ միջոցառումներ դեռ չկան։")
            return

        for item in rows:
            # aiogram Row → dict
            news_id = item["id"]
            title = item["title_hy"]
            eventdate = item.get("eventdate") or "Ոչ նշված"
            eventtime = item.get("eventtime") or "Ոչ նշված"
            venue = item.get("venue_hy") or "Ոչ նշված"
            price = item.get("price_hy")

            url = f"{BASE_URL}/hy/news/{news_id}"

            lines = [
                f"{title}",
                "",
                f"📅 {eventdate}",
                f"🕒 {eventtime}",
                f"📍 {venue}",
            ]
            if price:
                lines.append(f"💰 {price} դր.")
            lines.append("")
            lines.append(f"🔗 Մանրամասն՝ {url}")

            caption = "\n".join(lines)

            image_url = item.get("image_url")
            if image_url:
                await bot.send_photo(chat_id, photo=image_url, caption=caption)
            else:
                await bot.send_message(chat_id, caption)

        logger.info("✨ Holiday events sent to group")

    except Exception as e:
        logger.error(f"❌ Holiday events failed: {e}")
    finally:
        await bot.session.close()


# ================ 3. Չորեքշաբթի–կիրակի՝ հաջորդ օրվա event-ներ (09:00) ================

async def send_next_day_events():
    """
    Չորեքշաբթի–կիրակի 09:00 — ուղարկում է վաղվա event-ները DB-ից.
    ամեն event առանձին քարտանման մեսիջով AskYerevan link-ով։
    """
    bot = _get_bot()
    chat_id = _get_group_chat_id()

    try:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        rows = get_events_for_date(target_date=tomorrow, max_per_category=3)

        if not rows:
            logger.info("ℹ️ No events found for tomorrow")
            await bot.send_message(chat_id, "Վաղվա համար միջոցառումներ դեռ չկան։")
            return

        for item in rows:
            # aiogram Row → dict մուտք
            news_id = item["id"]
            title = item["title_hy"]

            eventdate = item.get("eventdate") or tomorrow.isoformat()
            eventtime = item.get("eventtime") or "Ոչ նշված"
            venue = item.get("venue_hy") or "Ոչ նշված"
            price = item.get("price_hy")

            url = f"{BASE_URL}/hy/news/{news_id}"

            lines = [
                f"{title}",
                "",
                f"📅 {eventdate}",
                f"🕒 {eventtime}",
                f"📍 {venue}",
            ]
            if price:
                lines.append(f"💰 {price} դր.")
            lines.append("")
            lines.append(f"🔗 Մանրամասն՝ {url}")

            caption = "\n".join(lines)

            image_url = item.get("image_url")
            if image_url:
                await bot.send_photo(chat_id, photo=image_url, caption=caption)
            else:
                await bot.send_message(chat_id, caption)

        logger.info("🎬 Next day events (from DB) sent to group")

    except Exception as e:
        logger.error(f"❌ Next day events failed: {e}")
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

async def notify_unanswered_questions():
    bot = _get_bot()
    try:
        rows = get_unanswered_questions_older_than(minutes=20)
        if not rows:
            return

        for q in rows:
            try:
                lang = q.get("user_lang") or "hy"
                ai_text = await generate_reply(q["text"], lang=lang)

                await bot.send_message(
                    chat_id=q["chat_id"],
                    text=ai_text,
                    reply_to_message_id=q["message_id"],
                )
                mark_question_answered(q["id"])
            except Exception as e:
                logger.exception(f"Auto‑reply failed for question id={q['id']}: {e}")
    finally:
        await bot.session.close()
