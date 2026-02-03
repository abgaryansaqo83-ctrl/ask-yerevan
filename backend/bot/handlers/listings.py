# backend/bot/handlers/listings.py
# ============================================
#   LISTINGS DETECTION (SELL / RENT / SEARCH / JOB)
# ============================================

from aiogram import Router, F
from aiogram.types import Message

from backend.utils.listings import detect_listing_category
from backend.utils.logger import logger
from backend.db import db  # async DB wrapper

router = Router()

# --------------------------------------------
# Group category mapping (edit if needed)
# --------------------------------------------
GROUP_CATEGORIES = {
    "sell": ["վաճառ", "sell"],
    "rent": ["վարձ", "rent"],
    "search": ["փնտր", "search"],
    "job": ["աշխատ", "job"],
}


def detect_group_category(title: str):
    """Detect group category based on chat title."""
    title = (title or "").lower()
    for cat, keys in GROUP_CATEGORIES.items():
        if any(k in title for k in keys):
            return cat
    return None


# --------------------------------------------
# Detect classified listings ONLY in groups
# --------------------------------------------
@router.message(F.text, F.chat.type.in_({"group", "supergroup"}))
async def detect_listings_handler(message: Message):
    """
    Detects if a message looks like a classified listing:
    - վաճառք
    - վարձով
    - փնտրում եմ
    - աշխատանք

    Works ONLY in group chats.
    """
    text = (message.text or "").strip().lower()
    if not text:
        return

    # Detect listing category from text
    detected_category = detect_listing_category(text)
    if not detected_category:
        return

    logger.info(
        f"Listing detected: user={message.from_user.id}, category={detected_category}, text={text}"
    )

    # Detect group category from chat title
    group_category = detect_group_category(message.chat.title)

    # --------------------------------------------
    # 1) Wrong group → block message
    # --------------------------------------------
    if group_category and group_category != detected_category:
        await message.reply(
            "❗ Այս հայտարարությունը պատկանում է այլ բաժնի։ "
            "Խնդրում եմ հրապարակեք համապատասխան խմբում։"
        )
        try:
            await message.delete()
        except Exception:
            pass
        return

    # --------------------------------------------
    # 2) Save listing to DB
    # --------------------------------------------
    await db.execute(
        """
        INSERT INTO listings (user_id, category, text)
        VALUES ($1, $2, $3)
        """,
        message.from_user.id,
        detected_category,
        text,
    )

    # --------------------------------------------
    # 3) If "search" → suggest matching listings
    # --------------------------------------------
    if detected_category == "search":
        # Extract a keyword (first meaningful word)
        keyword = text.split()[0]

        rows = await db.fetch(
            """
            SELECT user_id, text
            FROM listings
            WHERE category IN ('sell', 'rent')
              AND text ILIKE $1
            ORDER BY id DESC
            LIMIT 5
            """,
            f"%{keyword}%",
        )

        if rows:
            suggestions = "\n\n".join(f"• {r['text']}" for r in rows)
            await message.reply("💡 Ահա մի քանի համապատասխան տարբերակ.\n\n" + suggestions)

            # Notify sellers
            for r in rows:
                try:
                    await message.bot.send_message(
                        r["user_id"],
                        f"🔔 Մեկը փնտրում է այն, ինչ դուք հրապարակել էիք.\n\n"
                        f"Փնտրողից հաղորդագրություն՝\n{text}"
                    )
                except Exception:
                    pass
