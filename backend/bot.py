# bot.py

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config.settings import settings
from backend.utils.logger import logger

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


# ========== /start ==========

@dp.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message):
    text = (
        "Բարև, ես AskYerevan բոտն եմ 🙌\n"
        "Ի՞նչով կարող եմ օգնել։\n\n"
        "Գրիր՝ ինչ ես ուզում՝ եղանակ, խցանումներ, event, recommend, թե ուղղակի հարց։"
    )
    await message.answer(text)


# ========== /admin ==========

@dp.message(Command("admin", ignore_mention=True))
async def cmd_admin(message: Message):
    text = (
        "Ձեր գրած հաղորդագրությունը կուղարկվի ադմինիստրատորին "
        "անձնական նամակով և չի հրապարակվի AskYerevan խմբում։\n\n"
        "Խնդրում եմ, հաջորդ հաղորդագրությամբ գրեք ձեր հարցը կամ առաջարկը։"
    )
    await message.answer(text)

    # Այստեղ հետո կարող ենք FSM ավելացնել, որ հաջորդ մեսեջը forward անի admin chat-ին
    # օրինակ՝ await bot.send_message(settings.ADMIN_CHAT_ID, f"From {message.from_user.id}: {message.text}")


# ========== /news ==========

@dp.message(Command("news", ignore_mention=True))
async def cmd_news(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎬 Կինո", callback_data="news:film"),
                InlineKeyboardButton(text="🎭 Թատրոն", callback_data="news:theatre"),
            ],
            [
                InlineKeyboardButton(text="🎼 Օպերա", callback_data="news:opera"),
                InlineKeyboardButton(text="🍻 Փաբ / Փարթի", callback_data="news:party"),
            ],
            [
                InlineKeyboardButton(text="🎉 Event‑ներ", callback_data="news:festival"),
            ],
        ]
    )

    await message.answer(
        "Ընտրիր, թե ինչի մասին event‑ներ ես ուզում տեսնել․",
        reply_markup=keyboard,
    )


# ========== Սովորական տեքստեր (fallback router) ==========

@dp.message()
async def main_router(message: Message):
    text = (message.text or "").lower()

    # Greeting
    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    # Weather
    if "եղանակ" in text:
        await message.answer("Մի վայրկյան… եղանակը ստուգում եմ 🌤")
        return

    # Traffic
    if "ճանապարհ" in text or "փակ" in text or "խցանում" in text:
        await message.answer("Հիմա կստուգեմ Երևանի ճանապարհները… 🚗")
        return

    await message.answer("Հա, ասա՝ ինչ կա։")


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
