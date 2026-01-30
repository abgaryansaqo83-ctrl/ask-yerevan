# backend/bot/handlers/language.py
# ============================================
#   LANGUAGE SELECTION HANDLER
# ============================================

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from backend.database import save_user
from backend.utils.logger import logger

from ..states.language import LanguageForm


router = Router()


# --------------------------------------------
# Language selection keyboard
# --------------------------------------------
def build_language_keyboard():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇦🇲 Հայերեն", callback_data="lang:hy"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
            ]
        ]
    )


# --------------------------------------------
# Handle language selection (text-based)
# --------------------------------------------
@router.message(LanguageForm.waiting_for_choice)
async def handle_language_choice(message: Message, state: FSMContext):
    """
    User sends a text like "English", "Русский", "Հայերեն".
    We detect language and save it.
    """
    text = (message.text or "").strip().lower()

    if "rus" in text or "рус" in text:
        lang = "ru"
    elif "eng" in text or "english" in text:
        lang = "en"
    else:
        lang = "hy"

    logger.info(f"Language selected: {lang} by user={message.from_user.id}")

    save_user(
        chat_id=message.from_user.id,
        username=message.from_user.username or "",
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        language=lang,
    )

    responses = {
        "hy": "Լավ, քեզ հետ կխոսեմ հայերեն 😊",
        "ru": "Хорошо, буду общаться с тобой по-русски 😊",
        "en": "Great, I will talk to you in English 😊",
    }

    await message.answer(responses.get(lang, responses["hy"]), reply_markup=ReplyKeyboardRemove())
    await state.clear()
