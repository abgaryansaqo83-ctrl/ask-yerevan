import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from database import get_db_connection
from jobs import send_morning_broadcast, send_news_digest
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def start_scheduler():
    """Սկսում է բոտի background jobs-ները"""
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Yerevan'))
    
    # Առավոտյան հաղորդագրություն՝ 8:00-ին
    scheduler.add_job(
        send_morning_broadcast,
        CronTrigger(hour=8, minute=0, timezone=pytz.timezone('Asia/Yerevan')),
        id='morning_broadcast',
        replace_existing=True
    )
    
    # Նորությունների digest՝ 18:00-ին
    scheduler.add_job(
        send_news_digest,
        CronTrigger(hour=18, minute=0, timezone=pytz.timezone('Asia/Yerevan')),
        id='news_digest',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("✅ AskYerevanBot Scheduler started - Asia/Yerevan timezone")
    
    # Մշտապես աշխատում է
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(start_scheduler())

