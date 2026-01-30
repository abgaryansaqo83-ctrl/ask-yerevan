# backend/bot/handlers/admin.py
# ============================================
#   /admin — SEND MESSAGE TO ADMIN (PRIVATE)
# ============================================

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config.settings import settings
from backend.utils.logger import logger
from backend.languages import get_text

from ..states.admin import AdminForm


router = Router()


# --------------------------------------------
# /admin command — start admin message flow
# --------------------------------------------
@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    """
    User enters /admin → we switch to FSM and ask for the message.
    """
    lang = (message.from_user.language_code or "hy").lower()
    if lang.startswith("ru"):
        lang = "ru"
    elif lang.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    await message.answer(get_text("admin_intro", lang))
    await state.set_state(AdminForm.waiting_for_message)

    await message.answer(
        "Խնդրում եմ, հաջորդ հաղորդագրությամբ գրեք ձեր հարցը կամ առաջարկը։"
    )


# --------------------------------------------
# FSM: user sends message → forward to admin
# --------------------------------------------
@router.message(AdminForm.waiting_for_message)
async def process_admin_message(message: Message, state: FSMContext):
    """
    Takes the user's message and forwards it to ADMIN_CHAT_ID.
    """
    admin_chat_id = settings.ADMIN_CHAT_ID
    user = message.from_user

    username = f"@{user.username}" if user.username else "—"

    header = (
        "📩 Նոր admin հաղորդագրություն\n"
        f"👤 Անուն: {user.full_name}\n"
        f"🔹 Username: {username}\n"
        f"🆔 User ID: {user.id}\n"
        f"💬 From chat: {message.chat.id}\n\n"
    )

    # Forward to admin
    await message.bot.send_message(
        admin_chat_id,
        header + (message.text or "⬜️ (առանց տեքստի)"),
    )

    # If message came from group → delete it
    try:
        if message.chat.type in ("group", "supergroup"):
            await message.delete()
    except Exception:
        pass

    await message.answer(
        "Շնորհակալություն, ձեր հաղորդագրությունը ուղարկվեց ադմինին ✅\n"
        "Այն չի հրապարակվել խմբում։"
    )

    await state.clear()
