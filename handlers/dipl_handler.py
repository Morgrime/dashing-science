from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import KursStates, DiplStates
from keyboards.inlineKeyboards import support_kb, service_kb, cancel_kb, originality_diapason_kb, deadline_diapason_kb

"""
Димлом - хэдлер для начала рассчета стоимости диплома
"""
@router.callback_query(lambda c: c.data == 'dipl_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        await callback_query.message.answer('Вы выбрали диплом, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу')
    else:
        await callback_query.message.answer('Пожалуйста отмените работу или продолжите заполнять выбранную.')