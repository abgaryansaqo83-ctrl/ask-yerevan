# backend/bot/handlers/listings.py
# ============================================
#   LISTINGS DETECTION (SELL / RENT / SEARCH / JOB)
# ============================================

from aiogram import Router, F
from aiogram.types import Message

from backend.utils.listings import detect_listing_category
from backend.utils.logger import logger
from backend.database import (
    register_violation,
    count_violations,
    count_similar_listings,
    save_listing,
)
from backend.config.settings import settings

router = Router()


@router.message(F.text)
async def listings_router(message: Message):
    text_raw = (message.text or "").strip()
    if not text_raw:
        return

    # 0) Թողնենք commands-ը և հիմնական կոճակները մյուս routers-ին
    if text_raw.startswith("/"):
        return

    if text_raw in {
        "🌆 Քաղաքում ինչ կա՞",
        "🎟 Միջոցառումների մենյու",
        "💬 Հարց ադմինին",
        "🌐 Մեր վեբ կայքը",
    }:
        return

    text = text_raw.lower()
    thread_id = getattr(message, "message_thread_id", None)
    user_id = message.from_user.id

    # Քաղաքական spam filter
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

    if any(kw in text for kw in SPAM_POLITICS_KEYWORDS):
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

    # Listings detection (sell/rent/search/job)
    is_listing, category = detect_listing_category(text)
    if not is_listing:
        return

    # Thread checks
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

    # Frequency control
    repeats = count_similar_listings(user_id, text_raw, days=15)
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
        text=text_raw,
    )
