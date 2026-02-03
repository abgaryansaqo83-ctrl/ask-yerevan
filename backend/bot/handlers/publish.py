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


@router.message(Command("publish"))
async def publish_to_group_command(message: Message):
    logger.info(
        f"/publish command received from user_id={message.from_user.id}, OWNER_ID={OWNER_ID}"
    )

    if message.from_user.id != OWNER_ID:
        logger.warning(f"Unauthorized /publish attempt by {message.from_user.id}")
        await message.answer("❌ Այս հրամանը հասանելի է միայն բոտի տիրոջը։")
        return

    if not message.reply_to_message:
        logger.info("/publish: no reply message")
        await message.answer(
            "Խնդրում եմ reply արա այն հաղորդագրությանը, որը ուզում ես հրապարակել խմբում, "
            "հետո նոր գրի /publish։"
        )
        return

    reply = message.reply_to_message
    logger.info("/publish: reply message found")

    if not GROUP_CHAT_ID:
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
            await message.bot.send_message(chat_id=GROUP_CHAT_ID, text=reply.text)

        elif reply.photo:
            logger.info("/publish: sending photo")
            await message.bot.send_photo(
                chat_id=GROUP_CHAT_ID,
                photo=reply.photo[-1].file_id,
                caption=reply.caption or "",
            )

        elif reply.video:
            logger.info("/publish: sending video")
            await message.bot.send_video(
                chat_id=GROUP_CHAT_ID,
                video=reply.video.file_id,
                caption=reply.caption or "",
            )

        elif reply.document:
            logger.info("/publish: sending document")
            await message.bot.send_document(
                chat_id=GROUP_CHAT_ID,
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
