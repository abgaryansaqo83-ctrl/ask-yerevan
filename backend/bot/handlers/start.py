# backend/bot/handlers/start.py
# ============================================
#   START COMMAND / LANGUAGE DETECTION
# ============================================
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from backend.bot.keyboards.main_menu import build_main_keyboard
from backend.bot.states.user_question import UserQuestion
from backend.utils.logger import logger
from backend.languages import get_text
from backend.bot.handlers.utils import detect_lang  # սա կստեղծեմ հաջորդ քայլում

router = Router()

@router.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message, state: FSMContext):
    lang = detect_lang(message)

    await message.answer(
        get_text("start", lang),
        reply_markup=build_main_keyboard(),
    )

    await message.answer(
        "🌆 «Քաղաքում ինչ կա՞» — գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂\n"
        "🎟 «Միջոցառումների մենյու» — ընտրի՛ր, թե ինչ տեսակ event ես ուզում տեսնել․\n"
        "💬 «Հարց ադմինին» — գրի՛ հարցդ կամ առաջարկդ, և հաղորդագրությունը կուղարկվի ադմինին՝ "
        "առանց խմբում հրապարակվելու։\n"
        "🌐 «Մեր վեբ կայքը» — բացի AskYerevan կայքը։"
    )

    await state.set_state(UserQuestion.waiting_for_question)
