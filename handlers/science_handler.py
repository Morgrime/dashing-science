from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import ScienceStates, Universal
from keyboards.inlineKeyboards import cancel_kb, originality_diapason_kb, deadline_diapason_kb
from filters.filters import is_valid_text
from handlers.user_handler import TOTAL

router = Router()

user_dict: dict[int, dict[str, str | int | bool]] = {}

"""
Научная статья - хэдлер для начала рассчета стоимости научной статьи
"""
# вопрос про тему
@router.callback_query(lambda c: c.data == 'science_button', StateFilter(Universal.choice))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    TOTAL = 1500

    await callback_query.answer() 
    await callback_query.message.answer('Вы выбрали научную статью, пожалуйста ответьте на несколько вопросов, чтобы мы могли оценить вашу работу\n')
    await fill_theme(callback_query, state)

async def fill_theme(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Напишите тему вашей научной статьи.', reply_markup=cancel_kb)
    await state.set_state(ScienceStates.theme) # установления состояния "Тема"

# вопрос про процент оригинальности
@router.message(StateFilter(ScienceStates.theme), F.text.func(is_valid_text))    
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer('Какой процент оригинальности вы ожидаете?\n', 
                         reply_markup=originality_diapason_kb)
    await state.set_state(ScienceStates.originality) # установление состояния "Оригинальность"

# выбор диапазона оригинальности
@router.callback_query(F.data.in_(['fifty', 'sixty', 'seventy', 'eighty', 'ninety']), StateFilter(ScienceStates.originality))
async def choosen_diapason_of_originality(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    originality_costing = {
        'fifty': 0,
        'sixty': 150,
        'seventy': 200,
        'eighty': 300,
        'ninety': 400
    }
    originality_mapping = {
        'fifty': '50%+',
        'sixty': '60%+',
        'seventy': '70%+',
        'eighty': '80%+',
        'ninety': '90%+'
    }
    TOTAL += originality_costing[callback_query.data]
    await callback_query.answer() 
    await callback_query.message.answer(f'Вы выбрали оригинальность {originality_mapping[callback_query.data]}')
    await state.update_data(originality=originality_mapping[callback_query.data])
    await fill_deadline(callback_query, state)

async def fill_deadline(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Сколько дней осталось до сдачи работы?', reply_markup=deadline_diapason_kb)
    await state.set_state(ScienceStates.deadline)

# выбор дедлайна
@router.callback_query(F.data.in_(['1-3days', '4-7 days', '8-10days', '11-14days', '15days+']), StateFilter(ScienceStates.deadline))
async def chosen_diapason_of_deadline(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    deadline_costing = {
        '1-3days': 1000,
        '4-7days': 500,
        '8-10days': 300,
        '11-14days': 200,
        '15days+': 0
    }
    deadline_mapping = {
        '1-3days': '1-3 дней',
        '4-7days': '4-7 дней',
        '8-10days': '8-10 дней',
        '11-14days': '11-14 дней',
        '15days+': '15+ дней'
    }
    TOTAL += deadline_costing[callback_query.data]
    await callback_query.answer() 
    await callback_query.message.answer(f'У вас осталось {deadline_mapping[callback_query.data]}')
    await state.update_data(deadline=deadline_mapping[callback_query.data])
    await fill_wishes(callback_query, state)

async def fill_wishes(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Есть ли у вас какие-то пожелания к работе?')
    await state.set_state(ScienceStates.total)

"""
Проверка введённых данных
"""
# проверка на ̶в̶ш̶и̶в̶о̶с̶т̶ь̶  наличие текста
@router.message(StateFilter(ScienceStates.theme), lambda x: x.text.isdigit())
async def warning_not_text(message: Message):
    await message.answer('Пожалуйста, введите тему вашей научной статьи.')

# если в предыдущий хэндлер засунули что-то кроме оригинальности
@router.message(StateFilter(ScienceStates.originality))
async def warning_not_originality(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для того чтобы указать процент оригинальности.')

# если в предыдущий хэндлер засунули что-то кроме дедлайна
@router.message(StateFilter(ScienceStates.deadline))
async def warning_not_deadline(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для того чтобы указать сколько дней осталось до дедлайна,')   

"""
Тестовый возврат данных
"""
@router.message(StateFilter(ScienceStates.total))
async def get_all_data(message: Message, state: FSMContext):
    global TOTAL
    await state.update_data(wishes=message.text)
    user_dict[message.from_user.id] = await state.get_data() # все данные засовываются в словарь
    await state.clear()
    await message.answer(
        f'Тема - {user_dict[message.from_user.id]["theme"]}\n'
        f'Оригинальность - {user_dict[message.from_user.id]["originality"]}\n'
        f'Дней до сдачи - {user_dict[message.from_user.id]["deadline"]}\n'
        f'Пожелания - {user_dict[message.from_user.id]["wishes"]}\n\n'
        f'Итоговая стоимость - от {TOTAL}'
    )
    TOTAL = 0 