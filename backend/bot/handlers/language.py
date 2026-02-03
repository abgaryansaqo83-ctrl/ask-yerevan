# backend/bot/handlers/language.py
# ============================================
#   LANGUAGE SELECTION HANDLER
# ============================================

from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from backend.database import save_user
from backend.utils.logger import logger

from backend.bot.states.language import LanguageForm  # absolute import, ավելի պարզ [file:3]

router = Router()


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


@router.message(LanguageForm.waiting_for_choice)
async def handle_language_choice(message: Message, state: FSMContext):
    text = (message.text or "").strip().lower()

    if "rus" in text or "рус" in text:
        lang = "ru"
    elif "eng" in text or "english" in text:
        lang = "en"
    else:
        lang = "hy"

    logger.info(f"Language selected: {lang} by user={message.from_user.id}")

    # հին bot.py-ում save_user(...)–ը պահում էր user_id, username, full_name, language [file:3]
    save_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
        language=lang,
    )

    responses = {
        "hy": "Լավ, քեզ հետ կխոսեմ հայերեն 😊",
        "ru": "Хорошо, буду общаться с тобой по-русски 😊",
        "en": "Great, I will talk to you in English 😊",
    }

    await message.answer(responses.get(lang, responses["hy"]), reply_markup=ReplyKeyboardRemove())
    await state.clear()
