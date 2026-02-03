# backend/bot/handlers/news.py
# ============================================
#   /addnews — OWNER-ONLY NEWS CREATION (FSM)
# ============================================

import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from aiogram.fsm.context import FSMContext

from backend.database import save_news
from backend.utils.logger import logger
from backend.bot.states.addnews import AddNewsForm

router = Router()

OWNER_ID = int(os.getenv("OWNER_ID", "0"))


@router.message(Command("addnews"))
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


@router.message(AddNewsForm.waiting_for_title_hy)
async def process_title_hy(message: Message, state: FSMContext):
    await state.update_data(title_hy=message.text)
    await message.answer("2️⃣ Ուղարկիր վերնագիրը *անգլերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_title_en)


@router.message(AddNewsForm.waiting_for_title_en)
async def process_title_en(message: Message, state: FSMContext):
    await state.update_data(title_en=message.text)
    await message.answer("3️⃣ Ուղարկիր տեքստը *հայերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_content_hy)


@router.message(AddNewsForm.waiting_for_content_hy)
async def process_content_hy(message: Message, state: FSMContext):
    await state.update_data(content_hy=message.text)
    await message.answer("4️⃣ Ուղարկիր տեքստը *անգլերեն*", parse_mode="Markdown")
    await state.set_state(AddNewsForm.waiting_for_content_en)


@router.message(AddNewsForm.waiting_for_content_en)
async def process_content_en(message: Message, state: FSMContext):
    await state.update_data(content_en=message.text)
    await message.answer(
        "5️⃣ Ուղարկիր նկարը՝\n"
        "- կամ ուղարկիր *նկարի URL*\n"
        "- կամ ուղարկիր *ֆոտո*\n"
        "Կամ գրիր /skip, եթե չի պետք նկարը։",
        parse_mode="Markdown",
    )
    await state.set_state(AddNewsForm.waiting_for_image)


@router.message(AddNewsForm.waiting_for_image)
async def process_image(message: Message, state: FSMContext):
    data = await state.get_data()

    image_url = None
    photo_file_id = None

    if message.text == "/skip":
        image_url = None
    elif message.text and not message.photo:
        image_url = message.text.strip()
    elif message.photo:
        photo_file_id = message.photo[-1].file_id

    await state.update_data(
        image_url=image_url,
        photo_file_id=photo_file_id,
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 ԳԼԽԱՎՈՐ", callback_data="addnews:general")],
            [InlineKeyboardButton(text="🏙 ՔԱՂԱՔԱՅԻՆ", callback_data="addnews:city")],
            [InlineKeyboardButton(text="⚠️ ԿԱՐԵՎՈՐ", callback_data="addnews:important")],
        ]
    )

    await message.answer(
        "6️⃣ Ընտրիր կայքի բաժինը․\n\n"
        "🏠 ԳԼԽԱՎՈՐ — հիմնական նորություններ\n"
        "🏙 ՔԱՂԱՔԱՅԻՆ — քաղաքի առօրյա, ծառայություններ, միջոցառումներ\n"
        "⚠️ԿԱՐԵՎՈՐ — հատուկ / շտապ ինֆո",
        reply_markup=kb,
    )

    await state.set_state(AddNewsForm.waiting_for_category)


@router.callback_query(F.data.startswith("addnews:"), AddNewsForm.waiting_for_category)
async def process_addnews_category(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != OWNER_ID:
        await callback.answer("Այս հրամանը հասանելի է միայն տիրոջը։", show_alert=True)
        return

    category = callback.data.split(":", 1)[1]
    data = await state.get_data()

    title_hy = data["title_hy"]
    title_en = data["title_en"]
    content_hy = data["content_hy"]
    content_en = data["content_en"]
    image_url = data.get("image_url")
    photo_file_id = data.get("photo_file_id")

    if not image_url and photo_file_id:
        image_url = photo_file_id

    news_id = save_news(
        title_hy=title_hy,
        title_en=title_en,
        content_hy=content_hy,
        content_en=content_en,
        image_url=image_url,
        category=category,
    )

    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        f"✅ Նորությունը հրապարակվեց `{category}` բաժնում.\n"
        f"ID: {news_id}\n\n"
        "Տես վեբ կայքում՝ https://askyerevan.am/hy/news",
        parse_mode="Markdown",
    )

    await state.clear()
    await callback.answer("Պահպանվեց 🚀")
