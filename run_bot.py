import asyncio
from backend.bot.main import create_bot

async def main():
    bot, dp = create_bot()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
