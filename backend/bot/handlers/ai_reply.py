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

from ..states.question import UserQuestion


router = Router()

# User locations stored in memory (same as old bot.py)
USER_LOCATIONS: dict[int, str] = {}


# --------------------------------------------
# Helper: detect Armenian translit (optional)
# --------------------------------------------
def looks_like_armenian_translit(text: str) -> bool:
    """
    Detects if the user wrote Armenian using Latin letters.
    Used to improve AI understanding.
    """
    t = text.lower()

    # If Armenian letters already present → not translit
    if any("ա" <= ch <= "ֆ" for ch in t):
        return False

    keywords = [
        "barev", "barew", "inch", "inchka", "yerevan", "erevan",
        "jan", "shnorh", "lav", "sirum", "utelu", "xanut"
    ]
    return any(k in t for k in keywords)


# --------------------------------------------
# FSM: user asks a question after /start
# --------------------------------------------
@router.message(UserQuestion.waiting_for_question)
async def handle_user_question(message: Message, state: FSMContext):
    """
    Handles user questions:
    - Detects if it's a real question
    - Fetches recommendations (Google Places)
    - Fetches AI reply (Perplexity)
    - Combines both into one answer
    """
    raw = (message.text or "").strip()

    # Must contain a question mark
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

    # ----------------------------------------
    # 1) Try to get recommendations
    # ----------------------------------------
    rec_parts: list[str] = []
    try:
        recs = await get_recommendations(raw, user_location=user_location)
        if recs and not recs[0].startswith("🤔 "):
            rec_parts.extend(recs)
    except Exception as e:
        logger.error(f"Recommendation error: {e}")

    # ----------------------------------------
    # 2) AI reply (Perplexity)
    # ----------------------------------------
    ai_text = await generate_reply(raw, lang=lang)

    # ----------------------------------------
    # 3) Combine both
    # ----------------------------------------
    if rec_parts:
        full = "💡 Ահա մի քանի տարբերակ.\n" + "\n\n".join(rec_parts) + "\n\n" + ai_text
    else:
        full = ai_text

    await message.answer(full)
    await state.clear()


# --------------------------------------------
# Save user location for recommendations
# --------------------------------------------
@router.message(F.location)
async def handle_location(message: Message):
    """
    Saves user's last known location for better recommendations.
    """
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
