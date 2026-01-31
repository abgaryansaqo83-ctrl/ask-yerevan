# backend/bot/main.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from backend.config.settings import settings

# Import all routers
from .handlers.start import router as start_router
from .handlers.language import router as language_router
from .handlers.admin import router as admin_router
from .handlers.captcha import router as captcha_router
from .handlers.menu import router as menu_router
from .handlers.news import router as news_router
from .handlers.listings import router as listings_router
from .handlers.ai_reply import router as ai_reply_router
from .handlers.publish import router as publish_router


def create_bot():
    """
    Creates Bot + Dispatcher and registers all routers.
    This is the central entrypoint for the Telegram bot.
    """
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # Register routers
    dp.include_router(start_router)
    dp.include_router(language_router)
    dp.include_router(admin_router)
    dp.include_router(captcha_router)
    dp.include_router(menu_router)
    dp.include_router(news_router)
    dp.include_router(ai_reply_router)
    dp.include_router(publish_router)
    dp.include_router(listings_router)

    return bot, dp
