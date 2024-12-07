from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import Universal
from keyboards.inlineKeyboards import support_kb, service_kb

router = Router()

user_dict: dict[int, dict[str, str | int | bool]] = {}
TOTAL = 0

"""
Команда /start
"""
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer('Приветствую, я бот от Лихой Науки\n\n'
                        'Моя задача облегчить вам подбор нужной вам работы, а также её стоимость\n'
                        'Если будут вопросы - напишите команду /help')


"""
Инлайн-кнопка cancel - кнопка в меню для отмены заполнения работы
"""
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

@router.message(Command('cancel'))
async def process_cancel_menu_button(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer(text='Отменять нечего, пожалуйста выберите нужную услугу для расчета стоимости.\n'
                            'Для этого используйте /calculate')
    else:
        await message.answer(text='Отмена успешна')
        await state.clear()

"""
Кнопка help - объяснения как работать
"""
@router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('1) Нажмите на /calculate для рассчета стоимости\n'
                         '2) Вам зададут несколько уточняющих вопросов\n'
                         '3) После вопросов вам будет выдана примерная стоимость интересующей вам работы')


"""
Кнопка support - ссылки на меня, Ильнара или группу вк
"""
@router.message(Command('support'))
async def support_command(message: Message):
    await message.answer(text='Поддежка пользователя', 
                        reply_markup=support_kb)


"""
Кнопка calculate - выбрать услугу
"""
@router.message(Command('calculate'))
async def choose_service(message: Message, state: FSMContext):
    await message.answer(text='Выберите услугу',
                         reply_markup=service_kb)
    await state.set_state(Universal.choice)


"""
Хэндлер для ответа на незапланированные сообщения
"""
@router.message()
async def any_other_message(message: Message):
    await message.answer('Простите я не понял вас, используйте меню, либо команду /help')

