import asyncio,logging

from config import TOKEN
from aiogram import Bot, Dispatcher
from app import database as db
from app.handlers import router

bot = Bot(token=TOKEN)
dp=Dispatcher()


async def on_startup():
    print("Starting database setup...")
    await db.db_start()
    print("Database started")
async def main():
    dp.include_router(router)
    print("Bot started polling")
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping polling")