# backend/bot/handlers/menu.py
# ============================================
#   EVENTS MENU (/menu) + CALLBACK HANDLERS
# ============================================

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from backend.armenia.events import get_events_by_category, _format_event_line
from backend.utils.logger import logger


router = Router()


# --------------------------------------------
# /menu command — show event categories
# --------------------------------------------
@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """
    Shows the event categories menu with inline buttons.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎬 Կինո", callback_data="menu:film"),
                InlineKeyboardButton(text="🎭 Թատրոն", callback_data="menu:theatre"),
            ],
            [
                InlineKeyboardButton(text="🍻 Փաբ / ռեստորան", callback_data="menu:pub"),
                InlineKeyboardButton(text="🎤 Stand‑up", callback_data="menu:standup"),
            ],
            [
                InlineKeyboardButton(text="🎉 Միջոցառումներ", callback_data="menu:events"),
            ],
        ]
    )

    await message.answer("🎟 Միջոցառումների մենյու", reply_markup=keyboard)


# --------------------------------------------
# Callback handler for menu buttons
# --------------------------------------------
@router.callback_query(F.data.startswith("menu:"))
async def handle_menu_callback(callback: CallbackQuery):
    """
    Handles event category selection and sends 1–2 events.
    """
    try:
        await callback.answer()
    except Exception:
        pass  # Telegram sometimes throws "query is too old"

    kind = callback.data.split(":", 1)[1]
    logger.info(f"Menu callback: {kind}")

    events = await get_events_by_category(kind, limit=2)

    if not events:
        await callback.message.answer("😕 Այս պահին համապատասխան միջոցառումներ չեն գտնվել։")
        return

    for ev in events:
        caption = (
            _format_event_line(
                ev["title"],
                ev["venue"],
                ev["datetime"],
                ev["price"],
            )
            + f"\n\n🔗 Ավելին՝ {ev['more_url']}"
        )

        image_url = ev.get("image_url")

        # If DB has an image URL → send photo
        if image_url:
            try:
                await callback.message.answer_photo(photo=image_url, caption=caption)
            except Exception:
                await callback.message.answer(caption)
        else:
            await callback.message.answer(caption)
