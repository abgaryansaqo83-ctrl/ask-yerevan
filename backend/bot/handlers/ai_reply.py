# backend/bot/handlers/ai_reply.py
# ============================================
#   AI REPLY + RECOMMENDATIONS + TRANSLIT CHECK
# ============================================

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from backend.ai.response import generate_reply
from backend.armenia.recommend import get_recommendations
from backend.utils.logger import logger

from backend.bot.states.user_question import UserQuestion

router = Router()

USER_LOCATIONS: dict[int, str] = {}


def looks_like_armenian_translit(text: str) -> bool:
    t = text.lower()
    if any("ա" <= ch <= "ֆ" for ch in t):
        return False
    keywords = ["barev", "inch", "yerevan", "jan", "shnorh", "lav"]
    return any(k in t for k in keywords)


@router.message(UserQuestion.waiting_for_question, F.chat.type == "private")
async def handle_user_question(message: Message, state: FSMContext):
    raw = (message.text or "").strip()

    if "?" not in raw and "՞" not in raw:
        await message.answer("Գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂")
        return

    lang_code = (message.from_user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    user_id = message.from_user.id
    user_location = USER_LOCATIONS.get(user_id)

    logger.info(f"AI question from user={user_id}, lang={lang}, text={raw}")

    rec_parts = []
    try:
        recs = await get_recommendations(raw, user_location=user_location)
        if recs and not recs[0].startswith("🤔 "):
            rec_parts.extend(recs)
    except Exception as e:
        logger.error(f"Recommendation error: {e}")

    ai_text = await generate_reply(raw, lang=lang)

    if rec_parts:
        full = "💡 Ահա մի քանի տարբերակ.\n" + "\n\n".join(rec_parts) + "\n\n" + ai_text
    else:
        full = ai_text

    await message.answer(full)
    await state.clear()


@router.message(F.location, F.chat.type == "private")
async def handle_location(message: Message):
    loc = message.location
    if not loc:
        return

    user_id = message.from_user.id
    USER_LOCATIONS[user_id] = f"{loc.latitude},{loc.longitude}"

    await message.answer(
        "Ձեր դիրքը պահպանվեց ✅\n"
        "Հիմա երբ հարցնես, օրինակ՝ «որտե՞ղ գնանք սրճարան», "
        "կփորձեմ խորհուրդ տալ ավելի մոտ վայրեր։"
    )
