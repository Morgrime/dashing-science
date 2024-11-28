from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

# /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Приветствую, я бот от Лихой Науки\n\n'
                        'Моя задача облегчить вам подбор нужной вам работы, а также её стоимость\n'
                        'Если будут вопросы - напишите команду /help')
    
# /help
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('1) Выберите интересующую вас услугу в меню\n'
                         '2) Вам зададут несколько вопросов\n'
                         '3) После вопросов вам будет выдана примерная стоимость интересующей вам работы')

# /choose - выбрать услугу
@router.message(Command('choose_service'))
async def choose_service(message: Message):
    pass

# любое другое сообщение
@router.