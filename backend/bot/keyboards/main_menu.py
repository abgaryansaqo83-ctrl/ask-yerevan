# backend/bot/keyboards/main_menu.py
# ============================================
#   MAIN MENU KEYBOARD
# ============================================

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def build_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Main menu keyboard shown after /start.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌆 Քաղաքում ինչ կա՞")],
            [KeyboardButton(text="🎟 Միջոցառումների մենյու")],
            [KeyboardButton(text="💬 Հարց ադմինին")],
            [KeyboardButton(text="🌐 Մեր վեբ կայքը")],
            [KeyboardButton(text="📍 Ուղարկել դիրքս", request_location=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Ընտրի՛ր կոճակ կամ գրի՛ քո հարցը…",
    )
