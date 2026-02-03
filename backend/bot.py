# bot.py

import asyncio
import logging
import random
import os
import datetime
import signal

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
    ChatPermissions,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from backend.config.settings import settings
from backend.utils.logger import logger
from backend.languages import get_text
from backend.ai.response import generate_reply
from backend.utils.listings import detect_listing_category
from backend.database import (
    save_user,
    save_news,
    save_listing,
    register_violation,
    count_violations,
    count_similar_listings,
    init_db,
)
from backend.armenia.events import get_events_by_category, _format_event_line
from backend.armenia.recommend import get_recommendations
from transliterate import translit

init_db()

# ========== HELPERS ==========

def detect_lang(message: Message) -> str:
    code = (message.from_user.language_code or "hy").lower()
    if code.startswith("ru"):
        return "ru"
    if code.startswith("en"):
        return "en"
    return "hy"

USER_LOCATIONS: dict[int, str] = {}  # user_id -> "lat,lon"
BOT_SITE_URL = "https://askyerevan.am"
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()

def build_main_keyboard() -> ReplyKeyboardMarkup:
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

# ========== FSM STATES ==========

class LanguageForm(StatesGroup):
    waiting_for_choice = State()


class AdminForm(StatesGroup):
    waiting_for_message = State()


class UserQuestion(StatesGroup):
    waiting_for_question = State()


class CaptchaForm(StatesGroup):
    waiting_for_answer = State()

class AddNewsForm(StatesGroup):
    waiting_for_title_hy = State()
    waiting_for_title_en = State()
    waiting_for_content_hy = State()
    waiting_for_content_en = State()
    waiting_for_image = State()
    waiting_for_category = State()  # ՆՈՐ state — category ընտրության համար

# ========== Լեզվի ընտրություն ==========

@dp.message(LanguageForm.waiting_for_choice)
async def handle_language_choice(message: Message, state: FSMContext):
    text = (message.text or "").strip()

    if "Рус" in text or "рус" in text:
        lang = "ru"
    elif "English" in text or "Eng" in text:
        lang = "en"
    else:
        lang = "hy"

    save_user(
        user_id=message.from_user.id,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
        language=lang,
    )

    await message.answer(
        {
            "hy": "Լավ, քեզ հետ կխոսեմ հայերեն 😊",
            "ru": "Хорошо, буду общаться с тобой по-русски 😊",
            "en": "Great, I will talk to you in English 😊",
        }.get(lang, "Լավ, քեզ հետ կխոսեմ հայերեն 😊"),
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()

# ========== /start (bot) ==========

@dp.message(CommandStart(ignore_mention=True))
async def cmd_start(message: Message, state: FSMContext):
    lang = detect_lang(message)

    await message.answer(
        get_text("start", lang),
        reply_markup=build_main_keyboard(),
    )

    await message.answer(
        "🌆 «Քաղաքում ինչ կա՞» — գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂\n"
        "🎟 «Միջոցառումների մենյու» — ընտրի՛ր, թե ինչ տեսակ event ես ուզում տեսնել․\n"
        "💬 «Հարց ադմինին» — գրի՛ հարցդ կամ առաջարկդ, և հաղորդագրությունը կուղարկվի ադմինին՝ "
        "առանց խմբում հրապարակվելու։\n"
        "🌐 «Մեր վեբ կայքը» — բացի AskYerevan կայքը։"
    )

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

    # Խմբից ջնջում ենք հարցը, որ չմնա publishված
    try:
        if message.chat.type in ("group", "supergroup"):
            await message.delete()
    except Exception:
        pass

    await message.answer(
        "Շնորհակալություն, ձեր հաղորդագրությունը ուղարկվեց ադմինին ✅\n"
        "Այն չի հրապարակվել խմբում։"
    )

    await state.clear()


# ========== /menu command ==========

@dp.message(Command("menu", ignore_mention=True))
async def cmd_menu(message: Message):
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

    await message.answer(
        "🎟 Միջոցառումների մենյու",
        reply_markup=keyboard,
    )

# ========== /menu callback handler ==========

@dp.callback_query(F.data.startswith("menu:"))
async def handle_menu_callback(callback: CallbackQuery):
    try:
        await callback.answer()
    except Exception:
        pass  # եթե արդեն ուշ է, Telegram-ը կարող է գցել error, բայց դա crit չէ

    kind = callback.data.split(":", 1)[1]
    events = await get_events_by_category(kind, limit=2)

    if not events:
        await callback.message.answer("😕 Այս պահին համապատասխան միջոցառումներ չեն գտնվել։")
        return

    for ev in events:
        caption = _format_event_line(
            ev["title"],
            ev["venue"],
            ev["datetime"],
            ev["price"],
        ) + f"\n\n🔗 Ավելին՝ {ev['more_url']}"

        image_url = ev.get("image_url")

        # Եթե ունենք նկար DB-ից, ուղարկում ենք որպես photo, հակառակ դեպքում՝ մաքուր տեքստ
        if image_url:
            try:
                await callback.message.answer_photo(
                    photo=image_url,
                    caption=caption,
                )
            except Exception:
                # եթե նկարը չբեռնվի, fallback text-only
                await callback.message.answer(caption)
        else:
            await callback.message.answer(caption)


# ========== /site command ==========

@dp.message(Command("site", ignore_mention=True))
async def cmd_site(message: Message):
    await message.answer(f"🌐 AskYerevan վեբ էջը՝ {BOT_SITE_URL}")

# ========== CAPTCHA callback handler ==========

CAPTCHA_CORRECT = "lion"


@dp.callback_query(F.data.startswith("captcha:"), CaptchaForm.waiting_for_answer)
async def handle_captcha_answer(callback: CallbackQuery, state: FSMContext):
    choice = callback.data.split(":", 1)[1]
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    data = await state.get_data()
    attempts = int(data.get("captcha_attempts", 0))
    next_allowed_str = data.get("captcha_next_allowed")

    now = datetime.datetime.now(datetime.timezone.utc)

    if next_allowed_str:
        try:
            next_allowed = datetime.datetime.fromisoformat(next_allowed_str)
        except Exception:
            next_allowed = None
        if next_allowed and now < next_allowed:
            wait_hours = (next_allowed - now).total_seconds() // 3600 + 1
            await callback.answer(
                f"Հաջորդ փորձը հնարավոր կլինի մոտավորապես {int(wait_hours)} ժամից։",
                show_alert=True,
            )
            return

    if choice == CAPTCHA_CORRECT:
        await state.update_data(captcha_passed=True)

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
            ),
        )

        lang = "hy"
        welcome = get_text("welcome_new_member", lang).format(
            name=callback.from_user.full_name
        )
        combined = (
            "✅ Շնորհակալություն, թեստը հաջող անցար, հիմա կարող ես գրել խմբում։\n\n"
            + welcome
        )
        await callback.message.edit_text(combined)
        await callback.answer()

        kb = build_language_keyboard()
        await bot.send_message(
            callback.from_user.id,
            "Ընտրիր, թե որ լեզվով ես ուզում, որ բոտը քեզ հետ խոսի․",
            reply_markup=kb,
        )

        await state.set_state(LanguageForm.waiting_for_choice)
        return

    attempts += 1
    wait_hours = 0
    message_tail = ""

    if attempts == 1:
        wait_hours = 0
        message_tail = "Սա առաջին սխալ փորձն է, կարող ես նորից ընտրել։"
    elif attempts == 2:
        wait_hours = 8
        message_tail = "Սա երկրորդ սխալ փորձն է, հաջորդ հնարավորությունը կլինի 8 ժամից։"
    elif attempts == 3:
        wait_hours = 12
        message_tail = "Արդեն երեք սխալ փորձ կա, հաջորդ հնարավորությունը կլինի 12 ժամից։"
    elif attempts == 4:
        wait_hours = 24
        message_tail = (
            "Սա չորրորդ սխալ փորձն է։ Հաջորդը կլինի վերջինը և հասանելի կլինի 24 ժամից։"
        )
    else:
        await state.update_data(
            captcha_attempts=attempts,
            captcha_next_allowed=None,
            captcha_blacklisted=True,
        )
        await callback.answer(
            "Դու բազմակի անգամ սխալ ես ընտրել։ Հիմա խմբում կմնաս առանց գրելու հնարավորության, "
            "մինչև ադմինը որոշի բացել մուտքը։",
            show_alert=True,
        )
        return

    next_allowed = None
    if wait_hours > 0:
        next_allowed = now + datetime.timedelta(hours=wait_hours)

    await state.update_data(
        captcha_attempts=attempts,
        captcha_next_allowed=next_allowed.isoformat() if next_allowed else None,
    )

    await callback.answer(
        f"Սխալ ընտրություն է։ {message_tail}",
        show_alert=True,
    )

# ========== Նոր անդամ / լքող անդամ ==========

@dp.chat_member()
async def on_chat_member_update(event: ChatMemberUpdated, state: FSMContext):
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
    chat_id = event.chat.id

    lang_code = (user.language_code or "hy").lower()
    if lang_code.startswith("ru"):
        lang = "ru"
    elif lang_code.startswith("en"):
        lang = "en"
    else:
        lang = "hy"

    if new.status in ("member", "administrator") and old.status not in ("member", "administrator"):

        data = await state.get_data()
        if data.get("captcha_passed"):
            return

        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user.id,
            permissions=ChatPermissions(can_send_messages=False),
        )

        await send_captcha_test(chat_id, user.id, state, lang=lang)
        return

    if old.status in ("member", "administrator") and new.status in ("left", "kicked"):
        text = get_text("goodbye_member", lang).format(name=user.full_name)
        await bot.send_message(chat_id, text)
        return

# ========== /start-ից հետո AI հարց ==========

from transliterate import translit  # մի անգամ ավելացնել imports-ում

def looks_like_armenian_translit(text: str) -> bool:
    t = text.lower()
    # Եթե արդեն հայատառ կա, ոչինչ չենք անում
    if any("ա" <= ch <= "ֆ" for ch in t):
        return False
    # Armenian translit-ի ամենահաճախ հանդիպող patterns
    keywords = [
        "barev", "barew", "barev dzez",
        "inch", "inchka", "inch ka", "inchka e",
        "yerevan", "erevan", "ervan",
        "jan", "aj", "shnorh", "shnorakal", "merci", "vay", "lav em",
        "srt", "sirum", "friends", "toxi", "qayl", "utelu", "xanut"
    ]
    return any(k in t for k in keywords)


@dp.message(UserQuestion.waiting_for_question)
async def handle_user_question(message: Message, state: FSMContext):
    raw = (message.text or "").strip()
    lang = detect_lang(message)

    if "?" not in raw and "՞" not in raw:
        await message.answer("Գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂")
        return

    text = raw

    # User location, եթե ունենք
    user_id = message.from_user.id
    user_location = USER_LOCATIONS.get(user_id)

    # 1) Փորձում ենք recommendation-ներ բերել
    rec_parts: list[str] = []
    try:
        recs = await get_recommendations(raw, user_location=user_location)
        # recs always list[str]; եթե առաջինը «🤔 ...» է, значить category չի գտել
        if recs and not recs[0].startswith("🤔 "):
            rec_parts.extend(recs)
    except Exception:
        pass

    # 2) AI պատասխան
    reply = await generate_reply(text, lang=lang)

    # 3) Կոմբինացված պատասխան
    if rec_parts:
        full = "💡 Ահա մի քանի տարբերակ.\n" + "\n\n".join(rec_parts) + "\n\n" + reply
    else:
        full = reply

    await message.answer(full)
    await state.clear()


@dp.message(F.location)
async def handle_location(message: Message):
    """Պահում ենք user-ի վերջին դիրքը recommendations-ի համար."""
    loc = message.location
    if not loc:
        return

    user_id = message.from_user.id
    USER_LOCATIONS[user_id] = f"{loc.latitude},{loc.longitude}"

    await message.answer(
        "Ձեր դիրքը պահպանվեց ✅\n"
        "Հիմա երբ հարցնես, օրինակ՝ «որտե՞ղ գնանք սրճարան», կփորձեմ խորհուրդ տալ ավելի մոտ վայրեր։"
    )

# ========== Սովորական տեքստեր (fallback router) + /publish ==========

SPAM_POLITICS_KEYWORDS = [
    "քաղաքական", "կուսակց", "պատգամավոր", "կառավարություն", "իշխանություն",
    "ընդդիմություն", "վարչապետ", "նախագահ", "ընտրութ", "ընտրարշավ",
    "քարոզչ", "հանրաքվե", "սահմանադր", "ազգային ժողով", "կոռուպցիա",
    "իշխանափոխություն", "հեղափոխություն", "դիվանագիտ", "դեսպան",
    "պետականություն", "քաղաքական ուժ", "քաղաքական գործընթաց",
    "политик", "депутат", "правительств", "власть", "оппозиция",
    "партия", "выборы", "избирател", "агитац", "пропаганд",
    "референдум", "конституц", "коррупц", "смена власти",
    "революц", "дипломат", "президент", "премьер", "режим",
    "олигарх",
    "politic", "government", "opposition", "parliament", "senat",
    "election", "campaign", "vote", "voting", "referendum",
    "constitution", "corruption", "regime", "authoritarian",
    "oligarch", "diplomac", "propaganda", "lobby", "policy",
]

# ========== /publish (owner only) ==========

@dp.message(Command("publish"))
async def publish_to_group_command(message: Message):
    logger.info(
        f"/publish command received from user_id={message.from_user.id}, OWNER_ID={OWNER_ID}"
    )

    if message.from_user.id != OWNER_ID:
        logger.warning(f"Unauthorized /publish attempt by {message.from_user.id}")
        await message.answer("❌ Այս հրամանը հասանելի է միայն բոտի տիրոջը։")
        return

    logger.info("/publish: owner verified")

    if not message.reply_to_message:
        logger.info("/publish: no reply message")
        await message.answer(
            "Խնդրում եմ reply արա այն հաղորդագրությանը, որը ուզում ես հրապարակել խմբում, "
            "հետո նոր գրի /publish։"
        )
        return

    reply = message.reply_to_message
    logger.info("/publish: reply message found")

    group_chat_id = os.getenv("GROUP_CHAT_ID", "")
    logger.info(f"/publish: GROUP_CHAT_ID={group_chat_id}")

    if not group_chat_id:
        logger.error("/publish: GROUP_CHAT_ID is empty")
        await message.answer(
            "❌ GROUP_CHAT_ID փոփոխականը չի գտնվել Render-ի Environment Variables-ում։\n"
            "Մուտք գործիր Render dashboard → Environment և ավելացրու GROUP_CHAT_ID=քո խմբի ID‑ն։"
        )
        return

    try:
        logger.info("/publish: attempting to send message to group")

        if reply.text:
            logger.info("/publish: sending text message")
            await bot.send_message(chat_id=group_chat_id, text=reply.text)
        elif reply.photo:
            logger.info("/publish: sending photo")
            await bot.send_photo(
                chat_id=group_chat_id,
                photo=reply.photo[-1].file_id,
                caption=reply.caption or "",
            )
        elif reply.video:
            logger.info("/publish: sending video")
            await bot.send_video(
                chat_id=group_chat_id,
                video=reply.video.file_id,
                caption=reply.caption or "",
            )
        elif reply.document:
            logger.info("/publish: sending document")
            await bot.send_document(
                chat_id=group_chat_id,
                document=reply.document.file_id,
                caption=reply.caption or "",
            )
        else:
            logger.warning("/publish: unsupported message type")
            await message.answer(
                "Այս տեսակի հաղորդագրությունը դեռ չեմ կարող հրապարակել "
                "(պետք է լինի text, photo, video կամ document)։"
            )
            return

        logger.info("/publish: message published successfully")
        await message.answer("✅ Հաղորդագրությունը հրապարակվեց AskYerevan խմբում։")

    except Exception as e:
        logger.exception(f"/publish error: {e}")
        await message.answer(f"❌ Սխալ հրապարակելիս:\n{e}")

# ========== /addnews (owner only) — ԱՅՍՏԵՂ ==========

@dp.message(Command("addnews"))
async def cmd_addnews(message: Message, state: FSMContext):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Այս հրամանը հասանելի է միայն բոտի տիրոջը։")
        return

    await message.answer(
        "📰 Նոր նորություն ավելացնել\n\n"
        "1️⃣ Ուղարկիր վերնագիրը *հայերեն*",
        parse_mode="Markdown",
    )
    await state.set_state(AddNewsForm.waiting_for_title_hy)


@dp.message(AddNewsForm.waiting_for_title_hy)
async def process_title_hy(message: Message, state: FSMContext):
    await state.update_data(title_hy=message.text)
    await message.answer("2️⃣ Հիմա ուղարկիր վերնագիրը *անգլերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_title_en)


@dp.message(AddNewsForm.waiting_for_title_en)
async def process_title_en(message: Message, state: FSMContext):
    await state.update_data(title_en=message.text)
    await message.answer("3️⃣ Ուղարկիր տեքստը *հայերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_content_hy)


@dp.message(AddNewsForm.waiting_for_content_hy)
async def process_content_hy(message: Message, state: FSMContext):
    await state.update_data(content_hy=message.text)
    await message.answer("4️⃣ Ուղարկիր տեքստը *անգլերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_content_en)


@dp.message(AddNewsForm.waiting_for_content_en)
async def process_content_en(message: Message, state: FSMContext):
    await state.update_data(content_en=message.text)
    await message.answer(
        "5️⃣ Ուղարկիր նկարը՝\n"
        "- կամ ուղարկիր *նկարի URL*\n"
        "- կամ ուղարկիր *ֆոտո* (camera / gallery)\n"
        "Կամ գրիր /skip, եթե չի պետք նկարը։",
        parse_mode="Markdown",
    )
    await state.set_state(AddNewsForm.waiting_for_image)


# ===== Նկարների քայլ — URL կամ photo =====

@dp.message(AddNewsForm.waiting_for_image)
async def process_image(message: Message, state: FSMContext):
    """
    Այստեղ աջակցում ենք.
    - text => URL (կամ /skip)
    - photo => պահում ենք photo_file_id (Telegram-ում host եղած)
    """
    data = await state.get_data()

    image_url: str | None = None
    photo_file_id: str | None = None

    # Եթե user-ը գրել է /skip → բաց ենք թողնում նկարը
    if message.text == "/skip":
        image_url = None

    # Եթե ուղարկվածը տեքստ է (URL)
    elif message.text and not message.photo:
        image_url = message.text.strip()

    # Եթե ուղարկվածը իրական photo է (camera/gallery)
    elif message.photo:
        # վերցնում ենք ամենամեծ չափի photo-ի file_id
        photo_file_id = message.photo[-1].file_id

    # Պահում ենք FSM-ում
    await state.update_data(
        image_url=image_url,
        photo_file_id=photo_file_id,
    )

    # Category ընտրության կոճակները
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏠 ԳԼԽԱՎՈՐ", callback_data="addnews:general"),
            ],
            [
                InlineKeyboardButton(text="🏙 ՔԱՂԱՔԱՅԻՆ", callback_data="addnews:city"),
            ],
            [
                InlineKeyboardButton(text="⚠️ ԿԱՐԵՎՈՐ", callback_data="addnews:important"),
            ],
        ]
    )

    await message.answer(
        "6️⃣ Ընտրիր կայքի բաժինը․\n\n"
        "🏠 ԳԼԽԱՎՈՐ — հիմնական նորություններ\n"
        "🏙 ՔԱՂԱՔԱՅԻՆ — քաղաքի առօրյա, ծառայություններ, միջոցառումներ\n"
        "⚠️ ԿԱՐԵՎՈՐ — հատուկ / շտապ ինֆո",
        reply_markup=kb,
    )
    await state.set_state(AddNewsForm.waiting_for_category)


# ===== Category callback — իրական save դեպի DB =====

@dp.callback_query(F.data.startswith("addnews:"), AddNewsForm.waiting_for_category)
async def process_addnews_category(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        await callback.answer("Այս հրամանը հասանելի է միայն տիրոջը։", show_alert=True)
        return

    category = callback.data.split(":", 1)[1]  # general / city / important

    data = await state.get_data()

    title_hy = data["title_hy"]
    title_en = data["title_en"]
    content_hy = data["content_hy"]
    content_en = data["content_en"]
    image_url = data.get("image_url")
    photo_file_id = data.get("photo_file_id")  # եթե ֆոտո էր, սա լրացված կլինի

    # Այստեղ 2 տարբերակ ունես՝ ինչպես պահես նկարը DB-ի մեջ.
    # 1) Եթե backend / template-ը հարմարված է image_url-ի վրա,
    #    հիմա կարող ես արդեն անցնել ՊԱՐԶ վարիանտի՝ image_url-ում պահել հենց file_id,
    #    template-ում եթե սկսվում է "http" չէ, ապա image tag-ի փոխարեն
    #    օգտագործես Telegram-proxy կամ դեռ ոչինչ չցուցադրես։
    #
    # 2) Ավելի ճիշտ տարբերակ՝ bot-ում download անես ֆոտոն և upload անես
    #    քո media storage (S3, Render disk, և այլն) ու ստացած public URL-ը գրես image_url.
    #
    # Հիմա կթողնենք պարզ տարբերակը՝
    # - եթե user-ը ուղարկել է URL → image_url = URL
    # - եթե user-ը ուղարկել է photo → image_url = file_id (առանց download)
    # հետո, երբ media storage-դ պատրաստ լինի, կարող ես այս հատվածը փոխել՝
    # Telegram-ից download + backend upload logic դնելու համար. [web:270]

    if not image_url and photo_file_id:
        # պարզ պահեստավորում՝ file_id-ը պահում ենք image_url դաշտում
        image_url = photo_file_id

    news_id = save_news(
        title_hy=title_hy,
        title_en=title_en,
        content_hy=content_hy,
        content_en=content_en,
        image_url=image_url,
        category=category,
    )

    # Հանում ենք inline keyboard-ը, որ երկրորդ անգամ չսեղմեն
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        f"✅ Նորությունը հրապարակվեց `{category}` բաժնում.\n"
        f"ID: {news_id}\n\n"
        f"Տես վեբ կայքում՝ https://askyerevan.am/hy/news",
        parse_mode="Markdown",
    )

    await state.clear()
    await callback.answer("Պահպանվեց 🚀")
    

# ========== /sqlquery (owner only — database debug) ==========

@dp.message(Command("sqlquery"))
async def cmd_sqlquery(message: Message):
    """Owner only — Run SQL query on database"""
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Այս հրամանը հասանելի է միայն բոտի տիրոջը։")
        return
    
    from backend.database import get_connection, get_cursor
    
    query = message.text.replace("/sqlquery", "").strip()
    
    if not query:
        await message.answer(
            "📊 SQL Query\n\n"
            "Օրինակ՝\n"
            "`/sqlquery SELECT COUNT(*) FROM news;`\n"
            "`/sqlquery SELECT id, title_hy FROM news LIMIT 5;`",
            parse_mode="Markdown"
        )
        return
    
    try:
        conn = get_connection()
        cur = get_cursor(conn)
        cur.execute(query)
        
        # If SELECT query
        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            
            if not rows:
                await message.answer("📊 Արդյունքը՝ դատարկ է (0 տող)")
                conn.close()
                return
            
            # Format results
            result_text = f"📊 Գտնվեց {len(rows)} տող\n\n"
            for i, row in enumerate(rows[:10], 1):  # Max 10 rows
                result_text += f"{i}. {dict(row)}\n\n"
            
            if len(rows) > 10:
                result_text += f"... և ևս {len(rows) - 10} տող"
            
            await message.answer(result_text[:4000])  # Telegram limit
        else:
            # INSERT/UPDATE/DELETE
            conn.commit()
            await message.answer(f"✅ Query‑ը կատարվեց հաջողությամբ")
        
        conn.close()
    
    except Exception as e:
        await message.answer(f"❌ SQL Error:\n{str(e)[:500]}")

# ========== FALLBACK MESSAGE HANDLER ==========

@dp.message()
async def main_router(message: Message, state: FSMContext):
    logger.info(
        f"msg chat_id={message.chat.id}, "
        f"thread_id={getattr(message, 'message_thread_id', None)}, "
        f"text={message.text!r}"
    )

    text_raw = (message.text or "").strip()
    text = text_raw.lower()

    # 1) Ի՞նչ կա քաղաքում  → AI բոտ
    if text_raw == "🌆 Քաղաքում ինչ կա՞":
        await message.answer(
            "Գրի՛ քո հարցը Երևանի մասին, հարցականով 🙂"
            "Օրինակ՝ «Ճաշելու ի՞նչ հարմար սրճարան կա Ավանին մոտ», "
            "կամ «Ի՞նչ հետաքրքիր համերգներ կան այսօր»։"
        )
        await state.set_state(UserQuestion.waiting_for_question)
        return

    # 2) Միջոցառումների մենյու  → inline մենյու (կինո, թատրոն, փաբ…)
    if text_raw == "🎟 Միջոցառումների մենյու":
        await message.answer("Ընտրիր թե ի՞նչ տեսակի event ես ուզում տեսնել․")
        await cmd_menu(message)
        return

    # 3) Հարց ադմինին  → /admin flow
    if text_raw == "💬 Հարց ադմինին":
        await message.answer(
            "Գրի՛ քո հարցը կամ առաջարկը, և այն կուղարկվի ադմինին անձնական նամակով, "
            "առանց խմբում հրապարակվելու։"
        )
        await state.set_state(AdminForm.waiting_for_message)
        return

    # 4) Մեր վեբ կայքը  → ուղիղ լինկ
    if text_raw == "🌐 Մեր վեբ կայքը":
        await message.answer(
            f"🌐 Մեր վեբ կայքը՝ {BOT_SITE_URL}"
        )
        return

    if text_raw == "📍 Ուղարկել դիրքս":
        await message.answer(
            "Սեղմի՛ր նույն անունով կոճակը ստեղնաշարի վրա, Telegram-ը կառաջարկի "
            "ուղարկել դիրքդ (Share location)."
        )
        return

    if message.text and message.text.startswith("/"):
        return

    if message.from_user.id == settings.ADMIN_CHAT_ID:
        return

    text = (message.text or "").lower()
    thread_id = getattr(message, "message_thread_id", None)

    if thread_id == settings.FREE_CHAT_THREAD_ID:
        if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
            await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

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

    if any(word in text for word in ["բարև", "barev", "hi", "hello"]):
        await message.answer("Բարև՜, լսում եմ քեզ 🙂")
        return

    return

# ========== CAPTCHA helpers (keyboard + sender) ==========

def build_captcha_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="🐰", callback_data="captcha:rabbit"),
        InlineKeyboardButton(text="🐷", callback_data="captcha:pig"),
        InlineKeyboardButton(text="🐑", callback_data="captcha:lamb"),
        InlineKeyboardButton(text="🦁", callback_data="captcha:lion"),
    ]
    random.shuffle(buttons)
    return InlineKeyboardMarkup(inline_keyboard=[[b] for b in buttons])


async def send_captcha_test(chat_id: int, user_id: int, state: FSMContext, lang: str = "hy"):
    text_base = {
        "hy": "Ընտրիր այն կենդանուն, որին սովորաբար չեն ուտում 🧐",
        "ru": "Выбери животное, которого обычно не едят 🧐",
        "en": "Choose the animal people usually do NOT eat 🧐",
    }.get(lang, "Ընտրիր այն կենդանուն, որին սովորաբար չեն ուտում 🧐")

    mention = f"<a href=\"tg://user?id={user_id}\">օգտվող</a>"
    text = f"{mention}, {text_base}"

    kb = build_captcha_keyboard()
    await bot.send_message(chat_id, text, reply_markup=kb)
    await state.set_state(CaptchaForm.waiting_for_answer)


def build_language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🇦🇲 Հայերեն"),
                KeyboardButton(text="🇷🇺 Русский"),
                KeyboardButton(text="🇬🇧 English"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

# ========== ENTRYPOINT ==========

async def main():
    stop_event = asyncio.Event()

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        stop_event.set()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("AskYerevanBot started.")

    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted for clean start")

    polling_task = asyncio.create_task(dp.start_polling(bot))

    try:
        await stop_event.wait()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received.")
    finally:
        logger.info("Shutting down bot...")
        await dp.stop_polling()
        await bot.session.close()
        logger.info("Bot stopped successfully.")

if __name__ == "__main__":
    asyncio.run(main())
