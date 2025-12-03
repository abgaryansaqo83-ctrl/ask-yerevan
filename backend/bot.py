# bot.py

import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ChatMemberUpdated,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config.settings import settings
from backend.utils.logger import logger
from backend.languages import get_text
from backend.ai.response import generate_reply
from backend.utils.listings import detect_listing_category
from backend.database import (
    save_listing,
    register_violation,
    count_violations,
    count_similar_listings,
)
from backend.armenia.events_sources import get_today_events_by_category


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

    await message.answer(get_text("start", lang))

    text = (
        "Բարև, ես AskYerevan բոտն եմ 🙌\n"
        "Խոսում ենք Երևանի մասին՝ հետաքրքիր վայրեր և այլն։\n\n"
        "Հիմա գրի՛ քո հարցը՝ հատկապես եթե փնտրում ես ռեստորան, սրճարան, փաբ, "
        "հավես տեղ ընկերներով նստելու, թատրոն, կինոթատրոն կամ որևէ վայր Հայաստանում, "
        "ես էլ կփորձեմ գտնել ու օգնել ինչով կարող եմ։"
    )
    await message.answer(text)

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


@dp.callback_query(F.data.startswith("news:"))
async def handle_news_callback(callback: CallbackQuery):
    kind = callback.data.split(":", 1)[1]
    await callback.answer()

    if kind == "film":
        rows = get_today_events_by_category("cinema")
        if not rows:
            await callback.message.answer("Այսօր Երևանում կինոցուցադրության մասին ինֆո չունեմ 🙂")
            return

        lines = []
        for row in rows[:5]:
            line = (
                f"🎬 <b>{row['title']}</b>\n"
                f"📅 {row['date']} • 🕒 {row['time']}\n"
                f"📍 {row['place']}"
            )
            lines.append(line)

        await callback.message.answer("\n\n".join(lines))
        return

    mapping = {
        "theatre": "թատրոնի",
        "opera": "օպերայի",
        "party": "փաբների / փարթիների",
        "festival": "event‑ների",
    }
    label = mapping.get(kind, "event‑ների")

    await callback.message.answer(
        f"Հիմա դեռ test փուլում եմ {label} event‑ների համար, "
        f"շուտով կապ կհաստատեմ live աղբյուրների հետ և կսկսեմ բերել կոնկրետ միջոցառումներ։"
    )


# ========== Նոր անդամ / լքող անդամ ==========

@dp.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated):
    logger.info(
        "chat_member update: chat=%s user=%s old=%s new=%s",
        event.chat.id,
        event.new_chat_member.user.id,
        event.old_chat_member.status,
        event.new_chat_member.status,
    )

    old = event.old_chat_member
    new = event.new_chat_member
    user = new.user

    lang_code = (user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    chat_id = event.chat.id

    if new.status in ("member", "administrator") and old.status not in ("member", "administrator"):
        text = get_text("welcome_new_member", lang).format(name=user.full_name)
        await bot.send_message(chat_id, text)
        return

    if old.status in ("member", "administrator") and new.status in ("left", "kicked"):
        text = get_text("goodbye_member", lang).format(name=user.full_name)
        await bot.send_message(chat_id, text)
        return


# ========== /start-ից հետո AI հարց ==========

@dp.message(UserQuestion.waiting_for_question)
async def handle_user_question(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    lang = detect_lang(message)

    if "?" not in text and "՞" not in text:
        await message.answer("Եթե ուզում ես, որ անհատական քեզ օգնի բոտը, գրիր հարցդ հարցականով 🙂")
        return

    reply = await generate_reply(text, lang=lang)
    await message.answer(reply)
    await state.clear()


# ========== Սովորական տեքստեր (fallback router) ==========

SPAM_POLITICS_KEYWORDS = [
    # Հայերեն
    "քաղաքական", "կուսակց", "պատգամավոր", "կառավարություն", "իշխանություն",
    "ընդդիմություն", "վարչապետ", "նախագահ", "ընտրութ", "ընտրարշավ",
    "քարոզչ", "հանրաքվե", "սահմանադր", "ազգային ժողով", "կոռուպցիա",
    "իշխանափոխություն", "հեղափոխություն", "դիվանագիտ", "դեսպան",
    "պետականություն", "քաղաքական ուժ", "քաղաքական գործընթաց",

    # Русский
    "политик", "депутат", "правительств", "власть", "оппозиция",
    "партия", "выборы", "избирател", "агитац", "пропаганд",
    "референдум", "конституц", "коррупц", "смена власти",
    "революц", "дипломат", "президент", "премьер", "режим",
    "олигарх",

    # English
    "politic", "government", "opposition", "parliament", "senat",
    "election", "campaign", "vote", "voting", "referendum",
    "constitution", "corruption", "regime", "authoritarian",
    "oligarch", "diplomac", "propaganda", "lobby", "policy",
]


@dp.message()
async def main_router(message: Message):
    logger.info(
        f"msg chat_id={message.chat.id}, "
        f"thread_id={getattr(message, 'message_thread_id', None)}, "
        f"text={message.text!r}"
    )

    if message.from_user.id == settings.ADMIN_CHAT_ID:
        return

    text = (message.text or "").lower()
    thread_id = getattr(message, "message_thread_id", None)

    # Ազատ զրույց թեմա
    if thread_id == settings.FREE_CHAT_THREAD_ID:
        if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
            await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    # 1) Քաղաքական / սպամ filter
    if any(kw in text for kw in SPAM_POLITICS_KEYWORDS):
        user_id = message.from_user.id
        chat_id = message.chat.id

        register_violation(user_id, chat_id, "spam_politics")
        count = count_violations(user_id, chat_id, "spam_politics", within_hours=24)

        if count == 1:
            await message.reply(
                "Խումբը չի թույլատրում քաղաքական կամ սպամային հայտարարություններ։ "
                "Սա առաջին զգուշացումն է։ Կրկնվելու դեպքում գրելու հնարավորությունը "
                "կսահմանափակվի 24 ժամով։"
            )
            await message.delete()
            return

        if count == 2:
            await message.reply(
                "Կրկնվող քաղաքական/սպամային հայտարարության պատճառով "
                "ձեր գրելու հնարավորությունը սահմանափակվում է 24 ժամով։"
            )
            await message.delete()
            return

        if count >= 3:
            await message.reply(
                "Կանոնների բազմակի խախտման պատճառով դուք հեռացվում եք խմբից։ "
                "Վերադառնալ կարող եք միայն ադմինի հատուկ հղումով։"
            )
            await message.delete()
            return

    # 2) Հայտարարությունների վերահսկում
    is_listing, category = detect_listing_category(text)
    if is_listing:
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

        user_id = message.from_user.id
        repeats = count_similar_listings(user_id, message.text or "", days=15)

        if repeats >= 5:
            await message.reply(
                "Նույն հայտարարությունը հնարավոր է հրապարակել առավելագույնը 5 անգամ "
                "15 օրվա ընթացքում։ Խնդրում ենք սպասել, մինչև անցնի 15 օրը, "
                "և նոր միայն կրկին տեղադրել։"
            )
            await message.delete()
            return
        elif repeats == 4:
            await message.reply(
                "Զգուշացում․ այս հայտարարությունն արդեն գրեթե ամբողջությամբ "
                "օգտագործել է 15 օրվա 5 հրապարակման սահմանը։ "
                "Հաջորդ հրապարակումը կարող է արդեն արգելվել։"
            )

        save_listing(
            category=category,
            chat_id=message.chat.id,
            thread_id=thread_id,
            user_id=user_id,
            message_id=message.message_id,
            text=message.text or "",
        )
        return

    # 3) Պարզ բարև
    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    return


async def main():
    logger.info("AskYerevanBot started…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
