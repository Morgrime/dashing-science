from aiogram import Router, types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import KursStates, DiplStates
from keyboards.inlineKeyboards import support_kb, service_kb, cancel_kb

router = Router()

# /start
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Приветствую, я бот от Лихой Науки\n\n'
                        'Моя задача облегчить вам подбор нужной вам работы, а также её стоимость\n'
                        'Если будут вопросы - напишите команду /help')

"""
Инлайн-кнопка cancel
"""
# /cancel - кнопка в меню для отмены
@router.message(Command('cancel'), ~StateFilter(default_state))
async def menu_cancel_button(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        message.answer(text='Отменять нечего, пожалуйста выберите нужную услугу для расчета стоимости.\n'
                        'Для этого используйте /calculate')
    else:
        await message.answer(text='Работа отменена')
        await state.clear()

# TODO рассмотреть что тут можно написать
# инлайн-cancel который в зависимости от состояния будет или не будет отменять заполнение данных
@router.callback_query(lambda c: c.data == 'cancel_button')
async def process_cancel_button(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await callback_query.message.answer(
            text='Отменять нечего, пожалуйста выберите нужную услугу для расчета стоимости.\n'
                 'Для этого используйте /calculate')
    else:
        await callback_query.message.answer(text='Работа отменена')
        await state.clear()


"""
Кнопка help
"""
# /help
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('1) Нажмите на /calculate для рассчета стоимости\n'
                         '2) Вам зададут несколько уточняющих вопросов\n'
                         '3) После вопросов вам будет выдана примерная стоимость интересующей вам работы')

"""
Кнопка support
"""
# /support - ссылки на меня, Ильнара или группу вк
@router.message(Command('support'))
async def support_command(message: Message):
    await message.answer(text='Поддежка пользователя', 
                        reply_markup=support_kb)

"""
Кнопка calculate
"""
# /calculate - выбрать услугу
@router.message(Command('calculate'))
async def choose_service(message: Message):
    await message.answer(text='Выберите услугу',
                         reply_markup=service_kb)

"""
Курсовая
"""
# выбрана курсовая    
@router.callback_query(lambda c: c.data == 'kurs_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        await callback_query.message.answer('Вы выбрали курсовую, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу\n'
                                            'Напишите тему вашей курсовой работы', reply_markup=cancel_kb)
        await state.set_state(KursStates.theme) # тут сохраняется тема в FSM
    else:
        await callback_query.message.answer('Пожалуйста отмените работу или продолжите заполнять выбранную.')

@router.callback_query(lambda c: c.data == 'kurs_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Вы выбрали курсовую, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу\n'
                                        'Напишите тему вашей курсовой работы', reply_markup=cancel_kb)
    await state.set_state(KursStates.theme) # тут сохраняется тема в FSM

"""
Димлом
"""
# выбран диплом
@router.callback_query(lambda c: c.data == 'dipl_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        await callback_query.message.answer('Вы выбрали диплом, пожалуйста ответьте на несколько вопросов, чтобы я мог оценить вашу работу')
    else:
        await callback_query.message.answer('Пожалуйста отмените работу или продолжите заполнять выбранную.')

# любое другое сообщение
@router.message()
async def any_other_message(message: Message):
    await message.answer('Простите я не понял вас, используйте меню, либо команду /help')



# # /cancel который не будет работать если ничего не активно
# @router.message(Command(commands='cancel'), StateFilter(default_state))
# async def process_cancel_command(message: Message):
#     await message.answer(
#         text='Отменять нечего, пожалуйста выберите нужную услуга для рассчета стоимости.'
#         'Для этого используйте /calculate'
#     )


# # инлайн-cancel который не будет работать если ничего не активно
# @router.callback_query(lambda c: c.data == 'cancel_button', StateFilter(default_state))
# async def process_cancel_command(callback_query: types.CallbackQuery):
#     await callback_query.message.answer(
#         text='Отменять нечего, пожалуйста выберите нужную услуга для рассчета стоимости.'
#         'Для этого используйте /calculate'
#     )

# 
# # инлайн-cancel который будет работать если активно какое-то состояние
# @router.callback_query(lambda c: c.data == 'cancel_button', ~StateFilter(default_state))
# async def process_cancel_command(callback_query: types.CallbackQuery, state: FSMContext):
#     await callback_query.message.answer(
#         text='Работа отменена'
#     ) 
#     # состояние сброшено до по умолчанию
#     await state.clear() 
