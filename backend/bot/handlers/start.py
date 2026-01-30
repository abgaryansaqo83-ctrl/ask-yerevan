# backend/bot/handlers/start.py
# ============================================
#   START COMMAND / LANGUAGE DETECTION
# ============================================

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from backend.languages import get_text
from backend.utils.logger import logger

from ..keyboards.main_menu import build_main_keyboard
from ..states.question import UserQuestion


router = Router()


# --------------------------------------------
# Helper: Detect user language
# --------------------------------------------
def detect_lang(message: Message) -> str:
    """
    Detects Telegram user's language_code and normalizes it.
    Defaults to Armenian (hy).
    """
    code = (message.from_user.language_code or "hy").lower()

    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"
    return "hy"


# --------------------------------------------
# /start command handler
# --------------------------------------------
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """
    Sends greeting message + main menu keyboard.
    Then switches to UserQuestion FSM state.
    """
    lang = detect_lang(message)

    logger.info(f"/start from user={message.from_user.id}, lang={lang}")

    # Greeting text from backend/languages.py
    await message.answer(
        get_text("start", lang),
        reply_markup=build_main_keyboard(),
    )

    # Additional explanation message
    await message.answer(
        "🌆 «Քաղաքում ինչ կա՞» — գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂\n"
        "🎟 «Միջոցառումների մենյու» — ընտրի՛ր event-ի տեսակը\n"
        "💬 «Հարց ադմինին» — ուղարկում է անձնական նամակ ադմինին\n"
        "🌐 «Մեր վեբ կայքը» — բացում է AskYerevan կայքը"
    )

    # Switch FSM to question mode
    await state.set_state(UserQuestion.waiting_for_question)
