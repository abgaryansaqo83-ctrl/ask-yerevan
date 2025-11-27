import asyncio
from aiogram import Bot
from armenia.weather import get_yerevan_weather
from armenia.traffic import get_traffic_status
from ai.languages import get_morning_message
from database import get_active_users
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def send_morning_broadcast(bot_token: str):
    """8:00-ին ուղարկում է խմբում առավոտյան հաղորդագրություն բոլորին"""
    bot = Bot(token=bot_token)
    
    try:
        # Վերցնում ենք active users-ը DB-ից
        users = await get_active_users()
        logger.info(f"📢 AskYerevan Morning broadcast to {len(users)} users")

# Ֆայլի վերջում ավելացրու
async def send_test_broadcast(bot_token: str):
    """Admin-ի համար test broadcast"""
    logger.info("🧪 AskYerevanBot test broadcast")
    await send_morning_broadcast(bot_token)
        
        weather = await get_yerevan_weather()
        traffic = await get_traffic_status()
        
        for user in users:
            # Ըստ user-ի լեզվի
            message = await get_morning_message(
                user['language'], 
                weather=weather, 
                traffic=traffic
            )
            
            try:
                await bot.send_message(user['chat_id'], message)
                await asyncio.sleep(0.05)  # Rate limit
            except Exception as e:
                logger.error(f"Failed to send to {user['chat_id']}: {e}")
        
        await bot.session.close()
        logger.info("✅ Morning broadcast completed")
        
    except Exception as e:
        logger.error(f"❌ Morning broadcast failed: {e}")

async def send_news_digest(bot_token: str):
    """18:00-ին ուղարկում է օրվա նորությունները"""
    # Նմանատիպ լոգիկա, հետո կավելացնենք
    pass

