# run_bot.py

import asyncio
import signal

from backend.bot.main import create_bot
from backend.utils.logger import logger  # եթե ունես նույն logger-ը, ինչ հին bot.py-ում էր [file:3]


async def main():
    bot, dp = create_bot()

    # Հին bot.py-ում ունեիր webhook delete և graceful shutdown logic. [file:3]
    # Կարող ենք հիմնական մասը պահել.
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Webhook deleted for clean start")

    # Պոլլինգի Task
    polling_task = asyncio.create_task(dp.start_polling(bot))

    # Graceful shutdown signals
    stop_event = asyncio.Event()

    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        stop_event.set()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logger.info("AskYerevanBot started.")

    try:
        await stop_event.wait()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received.")
    finally:
        logger.info("Shutting down bot...")
        await dp.stop_polling()
        await bot.session.close()
        logger.info("Bot stopped successfully.")


if __name__ == "__main__":
    asyncio.run(main())
