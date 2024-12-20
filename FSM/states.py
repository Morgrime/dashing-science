from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

class KursStates(StatesGroup):
    theme = State()
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)

class DiplStates(StatesGroup):
    theme = State()
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)