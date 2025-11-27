from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# ---------------------------
# Main menu keyboard
# ---------------------------
def main_menu(lang="hy"):
    if lang == "hy":
        btn_weather = KeyboardButton("🌤 Եղանակ")
        btn_traffic = KeyboardButton("🚦 Ճանապարհային")
        btn_events = KeyboardButton("🎭 Իրադարձություններ")
        btn_recommend = KeyboardButton("🍽 Ո՞ւր գնալ ուտելու")
    else:
        btn_weather = KeyboardButton("Weather")
        btn_traffic = KeyboardButton("Traffic")
        btn_events = KeyboardButton("Events")
        btn_recommend = KeyboardButton("Food Recommendations")

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(btn_weather).add(btn_traffic).add(btn_events).add(btn_recommend)
    return kb


# ---------------------------
# Inline keyboard for yes/no
# ---------------------------
def yes_no_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Այո", callback_data="yes")],
            [InlineKeyboardButton(text="Ոչ", callback_data="no")],
        ]
    )


# ---------------------------
# Choose tone: Բաջի / Տատի
# ---------------------------
def tone_choice():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("👵 Տատի ոճ", callback_data="tone_tati")],
            [InlineKeyboardButton("👩‍🦳 Բաջի ոճ", callback_data="tone_baji")],
        ]
    )
