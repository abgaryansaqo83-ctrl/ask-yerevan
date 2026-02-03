# backend/bot/keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def build_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🌆 Քաղաքում ինչ կա՞"),
                KeyboardButton(text="🎟 Միջոցառումների մենյու"),
            ],
            [
                KeyboardButton(text="💬 Հարց ադմինին"),
                KeyboardButton(text="🌐 Մեր վեբ կայքը"),
            ],
            [
                KeyboardButton(text="📍 Ուղարկել իմ տեղադրությունը", request_location=True),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
