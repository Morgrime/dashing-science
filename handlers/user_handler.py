from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import KursStates, DiplStates
from keyboards.inlineKeyboards import support_kb, service_kb, cancel_kb, originality_diapason_kb, deadline_diapason_kb

router = Router()

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
async def choose_service(message: Message):
    await message.answer(text='Выберите услугу',
                         reply_markup=service_kb)


"""
Курсовая - хэдлер для начала рассчета стоимости курсовой
"""
# вопрос про тему
@router.callback_query(lambda c: c.data == 'kurs_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Вы выбрали курсовую, пожалуйста ответьте на несколько вопросов, чтобы мы могли оценить вашу работу\n'
                                        'Напишите тему вашей курсовой работы.', reply_markup=cancel_kb)
    # await state.update_data(theme=)
    await state.set_state(KursStates.theme) # установления состояния "Тема"

# проверка на ̶в̶ш̶и̶в̶о̶с̶т̶ь̶  наличие текста
@router.message(StateFilter(KursStates.theme), lambda x: x.text.isdigit())
async def warning_not_text(message: Message):
    await message.answer('Пожалуйста введите тему вашей курсовой.')

# вопрос про процент оригинальности
@router.message(StateFilter(KursStates.theme), F.text.isalpha())    
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer('Какой процент оригинальности вы ожидаете?\n'
                         'Можете выбрать из предложенных или ввести свой (от 40 до 100)', reply_markup=originality_diapason_kb)
    await state.set_state(KursStates.originality) # установление состояния "Оригинальность"

# вопрос про дедлайн
@router.message(StateFilter(KursStates.originality),
                lambda x: x.text.isdigit() and 40 <= int(x.text) <= 100)
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(originality=message.text)
    await message.answer('Сколько дней осталось до сдачи работы?', reply_markup=deadline_diapason_kb)
    await state.set_state(KursStates.deadline) # установление состояния "Дедлайн"

# если в предыдущий хэндлер засунули что-то кроме оригинальности
@router.message(StateFilter(KursStates.originality))
async def warning_not_originality(message: Message):
    await message.answer('Пожалуйста используйте кнопки для выбора процента оригинальности,'
                         'либо введите сами в диапазоне от 60 до 100')

# вопрос про пожелания к работе (необязательный)
@router.message(StateFilter(KursStates.deadline), lambda x: x.text.isdigit() and 1 <= int(x.text) <= 99999)    
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await message.answer('Ваши пожелания к работе? (данный пункт не обязателен)', reply_markup=cancel_kb)
    await state.set_state(KursStates.wishes) # установление состояния "Пожелания"

# если в предыдущий хэндлер засунули что-то кроме дедлайна
@router.message(StateFilter(KursStates.deadline))
async def warning_not_deadline(message: Message):
    await message.answer('Пожалуйста используйте кнопки для того чтобы указать сколько дней осталось до дедлайна,')

# тут возвращаются все данные
@router.message(StateFilter(KursStates.wishes))
async def get_all_data(message: Message, state: FSMContext):
    pass

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

"""
Хэндлер для ответа на незапланированные сообщения
"""
@router.message()
async def any_other_message(message: Message):
    await message.answer('Простите я не понял вас, используйте меню, либо команду /help')


# @router.message(Command('cancel'), ~StateFilter(default_state))
# async def menu_cancel_button(message: Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         message.answer(text='Отменять нечего, пожалуйста выберите нужную услугу для расчета стоимости.\n'
#                         'Для этого используйте /calculate')
#     else:
#         await message.answer(text='Работа отменена')
#         await state.clear()