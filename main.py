import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import BOT_TOKEN
from handlers.user_handler import router as user_router
from handlers.kurs_handler import router as kurs_router
from handlers.dipl_handler import router as dipl_router
from handlers.referat_handler import router as ref_router
from handlers.science_handler import router as science_router
from menu.menu  import set_main_menu
from logger.logger_config import format_1

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, format=format_1)

async def main():
     # инициализация хэндлеров
    dp.include_router(kurs_router)
    dp.include_router(dipl_router)
    dp.include_router(ref_router)
    dp.include_router(science_router)
    dp.include_router(user_router)
    dp.startup.register(set_main_menu) # инициализация кнопки меню

    await bot.delete_webhook(drop_pending_updates=True) # очистка старых недошедших сообщений
    await dp.start_polling(bot) # старт бота

if __name__ == "__main__":
    asyncio.run(main())