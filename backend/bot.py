import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from config.settings import settings
from backend.utils.logger import logger
from backend.languages import get_text


bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


@dp.message(Command("admin"))
async def admin_start(message: Message):
    text = (
        "կապ ադմինի հետ առաջարկների/բողոքների համար։\n"
        "Ձեր հաղորդագրությունը չի հրապարակվի խմբում, "
        "այլ կուղարկվի ուղիղ ադմինին անձնական նամակով.\n\n"
        "Խնդրում եմ գրիր քո հաղորդագրությունը հետևյալ հաղորդագրությամբ։"
    )
    await message.answer(text)



@dp.message()
async def main_router(message: Message):
    text = message.text.lower()

    # Greeting
    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    # Weather
    if "եղանակ" in text:
        await message.answer("Մի վայրկյան… եղանակը ստուգում եմ 🌤")
        return

    # Traffic
    if "ճանապարհ" in text or "փակ" in text:
        await message.answer("Հիմա կստուգեմ Երևանի ճանապարհները… 🚗")
        return

    await message.answer("Հա, ասա՝ ինչ կա։")


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
