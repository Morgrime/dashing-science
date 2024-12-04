from aiogram import Router, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import CalculatorStates
from keyboards.inlineKeyboards import support_keyboard, service_kb

router = Router()

# /start
@router.message(CommandStart(),  StateFilter(default_state))
async def start_command(message: Message):
    await message.answer('Приветствую, я бот от Лихой Науки\n\n'
                        'Моя задача облегчить вам подбор нужной вам работы, а также её стоимость\n'
                        'Если будут вопросы - напишите команду /help')
    
# /cancel который не будет работать если ничего не активно
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего, пожалуйста выберите нужную услуга для рассчета стоимости.'
        'Для этого используйте /calculate'
    )

# TODO рассмотреть что тут можно написать
# /cancel который будет работать если активно какое-то состояние
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(
        text='Работа отменена'
    ) 
    # состояние сброшено до по умолчанию
    await state.clear() 

# /help
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('1) Нажмите на /calculate для рассчета стоимости\n'
                         '2) Вам зададут несколько уточняющих вопросов\n'
                         '3) После вопросов вам будет выдана примерная стоимость интересующей вам работы')

# /support - ссылки на меня, Ильнара или группу вк
@router.message(Command('support'))
async def support_command(message: Message):
    await message.answer(text='Поддежка пользователя', 
                        reply_markup=support_keyboard)

# /choose - выбрать услугу
@router.message(Command('calculate'))
async def choose_service(message: Message):
    await message.answer(text='Выберите услугу',
                         reply_markup=service_kb)

"""
Курсовая
"""
# выбрана курсовая    
@router.callback_query(lambda c: c.data == 'kurs', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Вы выбрали курсовую, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу\n'
                                        'Напишите тему вашей курсовой работы')
    await state.set_state(CalculatorStates.theme) # тут сохраняется 





"""
Димлом
"""
# выбран диплом
@router.callback_query(lambda c: c.data == 'dipl')    
async def choose_kurs(callback_query: types.CallbackQuery):
    await callback_query.message.answer('Вы выбрали диплом, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу')

# любое другое сообщение
@router.message()
async def any_other_message(message: Message):
    await message.answer('Простите я не понял вас, используйте меню, либо команду /help')