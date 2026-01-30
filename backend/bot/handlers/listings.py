# backend/bot/handlers/listings.py
# ============================================
#   LISTINGS DETECTION (SELL / RENT / SEARCH / JOB)
# ============================================

from aiogram import Router
from aiogram.types import Message

from backend.utils.listings import detect_listing_category
from backend.utils.logger import logger


router = Router()


# --------------------------------------------
# Detect classified listings in user messages
# --------------------------------------------
@router.message()
async def detect_listings_handler(message: Message):
    """
    Detects if a message looks like a classified listing:
    - վաճառք
    - վարձով
    - փնտրում եմ
    - աշխատանք
    etc.

    If detected, logs it or handles it as needed.
    """
    text = (message.text or "").strip().lower()

    if not text:
        return

    category = detect_listing_category(text)

    if category:
        logger.info(
            f"Listing detected: user={message.from_user.id}, category={category}, text={text}"
        )
        # You can extend this logic later:
        # - save to DB
        # - notify admin
        # - auto-tag messages
        # For now we only log it.
