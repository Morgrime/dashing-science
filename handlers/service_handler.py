from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import default_state

service_router = Router()

# /kurs - начать калькулятор по курсовой
@service_router.message(Command('kurs'), StateFilter())
async def kurs_service_message(message: Message):
    pass