# backend/bot/handlers/publish.py
# ============================================
#   /publish — OWNER-ONLY MESSAGE PUBLISHING
# ============================================

import os
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from backend.utils.logger import logger


router = Router()

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID", "")


# --------------------------------------------
# /publish command (owner only)
# --------------------------------------------
@router.message(Command("publish"))
async def publish_to_group_command(message: Message):
    """
    Allows the bot owner to publish a replied message into the main group.
    """
    logger.info(
        f"/publish command from user_id={message.from_user.id}, OWNER_ID={OWNER_ID}"
    )

    # Owner check
    if message.from_user.id != OWNER_ID:
        logger.warning(f"Unauthorized /publish attempt by {message.from_user.id}")
        await message.answer("❌ Այս հրամանը հասանելի է միայն բոտի տիրոջը։")
        return

    # Must be reply
    if not message.reply_to_message:
        await message.answer(
            "Խնդրում եմ reply արա այն հաղորդագրությանը, որը ուզում ես հրապարակել խմբում, "
            "հետո նոր գրի /publish։"
        )
        return

    reply = message.reply_to_message

    if not GROUP_CHAT_ID:
        await message.answer(
            "❌ GROUP_CHAT_ID փոփոխականը չի գտնվել Render-ի Environment Variables-ում։"
        )
        return

    try:
        logger.info("/publish: sending message to group")

        # Text
        if reply.text:
            await message.bot.send_message(
                chat_id=GROUP_CHAT_ID,
                text=reply.text,
            )

        # Photo
        elif reply.photo:
            await message.bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=reply.photo[-1].file_id,
                caption=reply.caption or "",
            )

        # Video
        elif reply.video:
            await message.bot.send_video(
                chat_id=GROUP_CHAT_ID,
                video=reply.video.file_id,
                caption=reply.caption or "",
            )

        # Document
        elif reply.document:
            await message.bot.send_document(
                chat_id=GROUP_CHAT_ID,
                document=reply.document.file_id,
                caption=reply.caption or "",
            )

        else:
            await message.answer(
                "Այս տեսակի հաղորդագրությունը դեռ չեմ կարող հրապարակել "
                "(պետք է լինի text, photo, video կամ document)։"
            )
            return

        await message.answer("✅ Հաղորդագրությունը հրապարակվեց AskYerevan խմբում։")

    except Exception as e:
        logger.exception(f"/publish error: {e}")
        await message.answer(f"❌ Սխալ հրապարակելիս:\n{e}")
