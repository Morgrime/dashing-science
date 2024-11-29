from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

service_router = Router()

# /choose - выбрать услугу
@service_router.message(Command('choose_service'))
async def choose_service(message: Message):
    pass