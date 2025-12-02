# backend/scheduler.py

import asyncio
import signal
import sys
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

from .jobs import (
    send_morning_broadcast,
    send_week_premiere,
    # send_traffic_report,  # traffic job այլևս չունենք
    send_next_day_events,
    send_festival_events,
)
from .utils.logger import setup_logger
from config.settings import settings

logger = setup_logger(__name__)
TIMEZONE = ZoneInfo(settings.TIMEZONE)  # Asia/Yerevan


def create_scheduler() -> AsyncIOScheduler:
    """Scheduler-ի ստեղծում բոլոր job-ներով."""
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)

    # ================ ԱՄԵՆ ՕՐ ===================

    # 08:00 — Առավոտյան եղանակ (առանց խցանումների)
    scheduler.add_job(
        send_morning_broadcast,
        CronTrigger(hour=8, minute=0, timezone=TIMEZONE),
        id="morning_broadcast",
        replace_existing=True,
    )

    # ================ ԵՐԿՈՒՇԱԲԹԻ ===================

    # 08:30 — Շաբաթվա պրեմիերա
    scheduler.add_job(
        send_week_premiere,
        CronTrigger(day_of_week="mon", hour=8, minute=30, timezone=TIMEZONE),
        id="week_premiere",
        replace_existing=True,
    )

    # Այլևս ՉԿԱ 08:30 traffic_report job

    # ================ ՉՈՐԵՔՇԱԲԹԻ–ԿԻՐԱԿԻ ===================

    # 09:00 — Հաջորդ օրվա event-ներ (չորեքշաբթի–կիրակի)
    scheduler.add_job(
        send_next_day_events,
        CronTrigger(day_of_week="wed-sun", hour=9, minute=0, timezone=TIMEZONE),
        id="next_day_events",
        replace_existing=True,
    )

    # 09:30 — Փառատոններ (միայն չորեքշաբթի)
    scheduler.add_job(
        send_festival_events,
        CronTrigger(day_of_week="wed", hour=9, minute=30, timezone=TIMEZONE),
        id="festival_events",
        replace_existing=True,
    )

    logger.info("✅ Scheduler configured with all jobs")
    logger.info("📅 Active jobs:")
    for job in scheduler.get_jobs():
        try:
            run_time = getattr(job, "next_run_time", None)
            logger.info(f"  • {job.id} — next run: {run_time}")
        except Exception:
            logger.info(f"  • {job.id}")

    return scheduler


async def run_scheduler():
    """Scheduler-ի գործարկում + error handling."""
    scheduler = create_scheduler()

    def job_executed(event):
        logger.info(f"✅ Job {event.job_id} completed successfully")

    def job_error(event):
        logger.error(f"❌ Job {event.job_id} failed: {event.exception}")

    scheduler.add_listener(job_executed, EVENT_JOB_EXECUTED)
    scheduler.add_listener(job_error, EVENT_JOB_ERROR)

    def signal_handler(signum, frame):
        logger.info("🛑 Shutting down scheduler...")
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        scheduler.start()
        logger.info("🚀 Scheduler started. Press Ctrl+C to stop.")

        while True:
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("🛑 Scheduler stopped by user")
    except SystemExit:
        logger.info("🛑 Scheduler received SystemExit")
    finally:
        try:
            if scheduler.running:
                scheduler.shutdown()
        except Exception:
            pass
        logger.info("👋 Scheduler shutdown complete")


if __name__ == "__main__":
    asyncio.run(run_scheduler())
