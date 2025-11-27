import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.settings import settings
from backend.languages import get_text
from backend.utils.logger import logger


bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user.first_name

    text = (
        f"Բարև {user} 🌞\n\n"
        f"Դու կզբաղվես էն բոտով, որը պիտի դառնա Երևանցիների սիրելի օգնականը։\n"
        f"Ասա՝ ինչից սկսենք։"
    )

    await message.answer(text)


@dp.message()
async def main_handler(message: Message):
    text = message.text.lower()

    # Պարզ ռեակցիա՝ ստուգելու համար, որ ամեն ինչ OK է աշխատում
    if "բարև" in text or "barev" in text:
        await message.answer("Բարև ջան, Երևանից լսում եմ 🙂")
        return

    if "եղանակ" in text:
        await message.answer("Մի րոպե 👀… եղանակը հիմա կստուգեմ…")
        return

    await message.answer("Հա, լսում եմ քեզ։ Ի՞նչ ես ուզում։")


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

