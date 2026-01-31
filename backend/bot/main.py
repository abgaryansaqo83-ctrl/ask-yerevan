# backend/bot/main.py

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from backend.config.settings import settings

# Import all routers
from .handlers.start import router as start_router
from .handlers.language import router as language_router
from .handlers.admin import router as admin_router
from .handlers.menu import router as menu_router
from .handlers.ai_reply import router as ai_reply_router
from .handlers.news import router as news_router
from .handlers.publish import router as publish_router
from .handlers.captcha import router as captcha_router
from .handlers.listings import router as listings_router


def create_bot():
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # 1) START / LANGUAGE
    dp.include_router(start_router)
    dp.include_router(language_router)

    # 2) ADMIN
    dp.include_router(admin_router)

    # 3) MENU (events)
    dp.include_router(menu_router)

    # 4) AI reply (user questions)
    dp.include_router(ai_reply_router)

    # 5) NEWS / PUBLISH / CAPTCHA / LOCATION
    dp.include_router(news_router)
    dp.include_router(publish_router)
    dp.include_router(captcha_router)

    # 6) LISTINGS — ՎԵՐՋԻՆԸ
    dp.include_router(listings_router)

    return bot, dp
