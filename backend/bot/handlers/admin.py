# backend/bot/handlers/admin.py
# ============================================
#   /admin + "💬 Հարց ադմինին" BUTTON HANDLER
# ============================================

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from backend.config.settings import settings
from backend.languages import get_text
from backend.bot.states.admin import AdminForm

router = Router()


@router.message(F.text.contains("Հարց ադմինին"))
async def admin_button(message: Message, state: FSMContext):
    await cmd_admin(message, state)


@router.message(Command("admin", ignore_mention=True))
async def cmd_admin(message: Message, state: FSMContext):
    if message.chat.type != "private":
        return

    lang_code = (message.from_user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    await message.answer(get_text("admin_intro", lang))
    await state.set_state(AdminForm.waiting_for_message)

    text = (
        "Ձեր գրած հաղորդագրությունը կուղարկվի ադմինիստրատորին "
        "անձնական նամակով և չի հրապարակվի AskYerevan խմբում։\n\n"
        "Խնդրում եմ, հաջորդ հաղորդագրությամբ գրեք ձեր հարցը կամ առաջարկը։"
    )
    await message.answer(text)


# Եթե user-ը պատահմամբ գրում է խմբում այս state-ի տակ, ջնջում ենք
@router.message(
    AdminForm.waiting_for_message,
    F.chat.type.in_({"group", "supergroup"})
)
async def delete_admin_message_in_group(message: Message):
    try:
        await message.delete()
    except Exception:
        pass


@router.message(AdminForm.waiting_for_message)
async def process_admin_message(message: Message, state: FSMContext):
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

    await message.bot.send_message(
        admin_chat_id,
        header + (message.text or "⬜️ (առանց տեքստի)"),
    )

    await message.answer(
        "Շնորհակալություն, ձեր հաղորդագրությունը ուղարկվեց ադմինին ✅\n"
        "Այն չի հրապարակվել խմբում։"
    )

    await state.clear()
