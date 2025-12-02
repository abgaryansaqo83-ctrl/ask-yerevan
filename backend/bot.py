# bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F  # պետք կլինի, եթե հետո filters օգտագործենք

from config.settings import settings
from backend.utils.logger import logger
from backend.languages import get_text
from backend.ai.response import generate_reply
from backend.utils.listings import detect_listing_category
from backend.database import save_listing


def detect_lang(message: Message) -> str:
    code = (message.from_user.language_code or "hy").lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"
    return "hy"


bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


# ========== Admin FSM ==========

class AdminForm(StatesGroup):
    waiting_for_message = State()


# ========== User FSM (AI հարց) ==========

class UserQuestion(StatesGroup):
    waiting_for_question = State()


# ========== /start ==========

@dp.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message, state: FSMContext):
    lang = detect_lang(message)

    # Standard greeting from languages.py
    await message.answer(get_text("start", lang))

    # Լրացուցիչ բացատրություն flow-ի մասին
    text = (
        "Բարև, ես AskYerevan բոտն եմ 🙌\n"
        "Խոսում ենք Երևանի մասին՝ հետաքրքիր վայրեր և այլն։\n\n"
        "Հիմա գրի՛ քո հարցը՝ հատկապես եթե փնտրում ես ռեստորան, սրճարան, փաբ, "
        "հավես տեղ ընկերներով նստելու, թատրոն, կինոթատրոն կամ որևէ վայր Հայաստանում, "
        "ես էլ կփորձեմ գտնել ու օգնել ինչով կարող եմ։"
    )
    await message.answer(text)

    # Մի հարցի սպասման վիճակ
    await state.set_state(UserQuestion.waiting_for_question)


# ========== /admin ==========

@dp.message(Command("admin", ignore_mention=True))
async def cmd_admin(message: Message, state: FSMContext):
    lang = detect_lang(message)
    await message.answer(get_text("admin_intro", lang))
    await state.set_state(AdminForm.waiting_for_message)

    text = (
        "Ձեր գրած հաղորդագրությունը կուղարկվի ադմինիստրատորին "
        "անձնական նամակով և չի հրապարակվի AskYerevan խմբում։\n\n"
        "Խնդրում եմ, հաջորդ հաղորդագրությամբ գրեք ձեր հարցը կամ առաջարկը։"
    )
    await message.answer(text)


@dp.message(AdminForm.waiting_for_message)
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

@dp.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated):
    old = event.old_chat_member
    new = event.new_chat_member
    user = new.user

    # Լեզուն հիմա կարող ենք վերցնել user.language_code-ից
    lang_code = (user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    # Նոր անդամ է միացել
    if old.status in ("left", "kicked") and new.status in ("member", "administrator"):
        text = get_text("welcome_new_member", lang).format(name=user.full_name)
        await event.chat.send_message(text)
        return

    # Մասնակիցը դուրս է եկել կամ հեռացվել է
    if old.status in ("member", "administrator") and new.status in ("left", "kicked"):
        text = get_text("goodbye_member", lang).format(name=user.full_name)
        await event.chat.send_message(text)
        return

# ========== UserQuestion state-ի handler (AI) ==========

@dp.message(UserQuestion.waiting_for_question)
async def handle_user_question(message: Message, state: FSMContext):
    """
    /start-ից հետո եկող առաջին հարցականով մեսիջը.
    Այստեղ է, որ AI-ին ենք ուղարկում հարցը և հետո state-ը մաքրում։
    """
    text = (message.text or "").strip()
    lang = detect_lang(message)

    # Եթե սա իրական հարց չէ (չի պարունակում '?' կամ '՞'), treat as ordinary message
    if "?" not in text and "՞" not in text:
        await message.answer("Եթե ուզում ես, որ անհատական քեզ օգնի բոտը, գրիր հարցդ հարցականով 🙂")
        return

    # AI reply
    reply = await generate_reply(text, lang=lang)
    await message.answer(reply)

    # Մի հարցին պատասխանելուց հետո state reset
    await state.clear()


# ========== Սովորական տեքստեր (fallback router) ==========

@dp.message()
async def main_router(message: Message):
    logger.info(
        f"msg chat_id={message.chat.id}, "
        f"thread_id={getattr(message, 'message_thread_id', None)}, "
        f"text={message.text!r}"
    )

    # 0) Admin bypass — քո վրա ոչ մի սահմանափակում չի աշխատում
    if message.from_user.id == settings.ADMIN_CHAT_ID:
        return

    text = (message.text or "").lower()
    thread_id = getattr(message, "message_thread_id", None)

    # -------- 1) հայտարարությունների վերահսկում --------
    is_listing, category = detect_listing_category(text)

    if is_listing:
        # Սխալ բաժիններ
        if category == "sell" and thread_id != settings.SELL_THREAD_ID:
            await message.reply(
                "Սա վաճառքի հայտարարություն է, խնդրում եմ տեղադրեք «Վաճառք» բաժնում 🙂"
            )
            await message.delete()
            return

        if category == "rent" and thread_id != settings.RENT_THREAD_ID:
            await message.reply(
                "Սա վարձակալության հայտարարություն է, խնդրում եմ տեղադրեք «Վարձու» բաժնում 🙂"
            )
            await message.delete()
            return

        if category == "search" and thread_id != settings.SEARCH_THREAD_ID:
            await message.reply(
                "Սա «Փնտրում եմ» հայտարարություն է, խնդրում եմ տեղադրեք «Փնտրում եմ» բաժնում 🙂"
            )
            await message.delete()
            return

        if category == "job_offer" and thread_id != settings.JOB_SERVICE_THREAD_ID:
            await message.reply(
                "Սա աշխատանքի կամ ծառայության առաջարկ է, խնդրում եմ տեղադրեք համապատասխան բաժնում 🙂"
            )
            await message.delete()
            return

        # Ճիշտ բաժին է՝ պահում ենք DB-ում (հետո կավելացնենք matching-ը)
        save_listing(
            category=category,
            chat_id=message.chat.id,
            thread_id=thread_id,
            user_id=message.from_user.id,
            message_id=message.message_id,
            text=message.text or "",
        )
        return

    # -------- 2) մնացած logic-ը, որը արդեն ունեիր --------

    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    # Այլ դեպքերում բոտը լռում է
    return


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
