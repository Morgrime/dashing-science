import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import BOT_TOKEN
from handlers.user_handler import router
from menu.menu  import set_main_menu
from logger.logger_config import format_1

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, format=format_1)

async def main():
    dp.include_router(router) # инициализация хэндлеров
    dp.startup.register(set_main_menu) # инициализация кнопки меню

    await bot.delete_webhook(drop_pending_updates=True) # очистка старых недошедших сообщений
    await dp.start_polling(bot) # старт бота

if __name__ == "__main__":
    asyncio.run(main())