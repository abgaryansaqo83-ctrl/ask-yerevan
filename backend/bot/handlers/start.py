# backend/bot/handlers/start.py
# ============================================
#   START COMMAND / MAIN MENU BUTTON HANDLERS
# ============================================

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from backend.bot.keyboards.main_menu import build_main_keyboard
from backend.bot.states.user_question import UserQuestion
from backend.languages import get_text
from backend.bot.handlers.utils import detect_lang

router = Router()


@router.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message, state: FSMContext):
    lang = detect_lang(message)

    # GROUP CHAT → no keyboard, no FSM
    if message.chat.type != "private":
        await message.answer(get_text("start", lang))
        return

    # PRIVATE CHAT → full menu + FSM
    await message.answer(
        get_text("start", lang),
        reply_markup=build_main_keyboard(),
    )

    await message.answer(
        "🌆 «Քաղաքում ինչ կա՞» — գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂\n"
        "🎟 «Միջոցառումների մենյու» — ընտրի՛ր event տեսակը\n"
        "💬 «Հարց ադմինին» — ուղարկվում է ադմինին, չի հրապարակվում խմբում\n"
        "🌐 «Մեր վեբ կայքը» — բացում է AskYerevan կայքը"
    )

    await state.set_state(UserQuestion.waiting_for_question)


@router.message(F.text == "🌆 Քաղաքում ինչ կա՞")
async def handle_city_button(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return
    await message.answer("Գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂")
    await state.set_state(UserQuestion.waiting_for_question)


@router.message(F.text == "🌐 Մեր վեբ կայքը")
async def handle_website_button(message: Message):
    await message.answer("🌐 AskYerevan կայքը՝ https://askyerevan.am")
