from aiogram import Bot
from aiogram.types import BotCommand

# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/calculate',
                   description='Посчитать стоимость работы'),
        BotCommand(command='/support',
                   description='Связаться с техподдержкой'),
        BotCommand(command='/cancel',
                   description='Отмена')
    ]

    await bot.set_my_commands(main_menu_commands)