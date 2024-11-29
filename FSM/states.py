from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup

class FSMcount(StatesGroup):
    fill_days_remaining = State()
    fill_originality = State()
    fill_characters = State()