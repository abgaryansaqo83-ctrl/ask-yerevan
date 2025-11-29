# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config.settings import settings
from backend.utils.logger import logger


bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


# ========== Admin FSM ==========

class AdminForm(StatesGroup):
    waiting_for_message = State()


# ========== /start ==========

@dp.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message):
    text = (
        "Բարև, ես AskYerevan բոտն եմ 🙌\n"
        "Խոսում ենք Երևանի մասին՝ հետաքրքիր վայրեր և այլն։\n\n"
        "Կուզե՞ս ուղղակի հարց տուր կամ գրիր ինչ վայր ես փնտրում՝ ռեստորան, սրճարան, փաբ, "
        "հավես տեղ ընկերներով նստելու, ես էլ կփորձեմ գտնել ու օգնել ինչով կարող եմ։"
    )
    await message.answer(text)


# ========== /admin ==========

@dp.message(Command("admin", ignore_mention=True))
async def cmd_admin(message: Message, state: FSMContext):
    text = (
        "Ձեր գրած հաղորդագրությունը կուղարկվի ադմինիստրատորին "
        "անձնական նամակով և չի հրապարակվի AskYerevan խմբում։\n\n"
        "Խնդրում եմ, հաջորդ հաղորդագրությամբ գրեք ձեր հարցը կամ առաջարկը։"
    )
    await message.answer(text)
    await state.set_state(AdminForm.waiting_for_message)


@dp.message(AdminForm.waiting_for_message)
async def process_admin_message(message: Message, state: FSMContext):
    admin_chat_id = settings.ADMIN_CHAT_ID

    user = message.from_user
    header = (
        "📩 Նոր admin հաղորդագրություն\n"
        f"from: {user.full_name} (id={user.id})\n"
        f"chat: {message.chat.id}\n\n"
    )

    await bot.send_message(
        admin_chat_id,
        header + (message.text or "⬜️ (առանց տեքստի)"),
    )
    await message.answer("Շնորհակալություն, ձեր հաղորդագրությունը ուղարկվեց ադմինին ✅")

    await state.clear()


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

    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    if "եղանակ" in text:
        await message.answer("Մի վայրկյան… եղանակը ստուգում եմ 🌤")
        return

    if "ճանապարհ" in text or "փակ" in text or "խցանում" in text:
        await message.answer("Հիմա կստուգեմ Երևանի ճանապարհները… 🚗")
        return

    await message.answer("Հա, ասա՝ ինչ կա։")


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
