import asyncio

from aiogram import Bot, Dispatcher
from config.config import BOT_TOKEN, ADMIN_IDS
from handlers.user_handler import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True) # очистка старых недошедших сообщений
    await dp.start_polling(bot) # старт бота

if __name__ == "__main__":
    asyncio.run(main())