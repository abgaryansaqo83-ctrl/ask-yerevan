import asyncio
import os
from aiogram import Bot
from armenia.weather import get_yerevan_weather
from armenia.traffic import get_traffic_status
from ai.response import generate_morning_tone
from database import get_active_users
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def send_morning_broadcast():
    """8:00 AskYerevan Morning Broadcast"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    group_chat_id = int(os.getenv('GROUP_CHAT_ID', '-1001234567890'))
    bot = Bot(token=bot_token)
    
    try:
        # Real data
        weather = await get_yerevan_weather(os.getenv('OPENWEATHER_KEY'))
        traffic = await get_traffic_status(os.getenv('GOOGLE_DIRECTIONS_KEY'))
        
        # AI tone generation (բաժի/տատի ոճով)
        message = await generate_morning_tone(weather, traffic)
        
        await bot.send_message(group_chat_id, message)
        logger.info("✅ AskYerevan Morning broadcast sent to group")
        
    except Exception as e:
        logger.error(f"❌ Morning broadcast failed: {e}")
    finally:
        await bot.session.close()

async def send_test_broadcast():
    """Admin test button"""
    await send_morning_broadcast()
    logger.info("🧪 Test broadcast completed")
