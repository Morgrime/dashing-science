from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import DiplStates, Universal
from keyboards.inlineKeyboards import cancel_kb, originality_diapason_kb, deadline_diapason_kb
from filters.filters import is_valid_text
from handlers.user_handler import TOTAL

router = Router()

user_dict: dict[int, dict[str, str | int | bool]] = {}

"""
Дипломная - хэдлер для начала рассчета стоимости дипломной работы
"""
# вопрос про тему
@router.callback_query(lambda c: c.data == 'dipl_button', StateFilter(Universal.choice))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    TOTAL = 10000
    await callback_query.message.answer('Вы выбрали дипломную работу, пожалуйста ответьте на несколько вопросов, чтобы мы могли оценить вашу работу\n')
    await fill_theme(callback_query, state)

async def fill_theme(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Напишите тему вашей дипломной работы работы.', reply_markup=cancel_kb)
    await state.set_state(DiplStates.theme) # установления состояния "Тема"

# вопрос про процент оригинальности
@router.message(StateFilter(DiplStates.theme), F.text.func(is_valid_text))    
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer('Какой процент оригинальности вы ожидаете?\n', 
                         reply_markup=originality_diapason_kb)
    await state.set_state(DiplStates.originality) # установление состояния "Оригинальность"

# выбор диапазона оригинальности
@router.callback_query(F.data.in_(['sixty', 'seventy', 'eighty', 'ninety']), StateFilter(DiplStates.originality))
async def choosen_diapason_of_originality(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    originality_costing = {
        'sixty': 3000,
        'seventy': 4500,
        'eighty': 6000,
        'ninety': 7500
    }
    originality_mapping = {
        'sixty': '60%+',
        'seventy': '70%+',
        'eighty': '80%+',
        'ninety': '90%+'
    }
    TOTAL += originality_costing[callback_query.data]
    await callback_query.message.answer(f'Вы выбрали оригинальность {originality_mapping[callback_query.data]}')
    await state.update_data(originality=originality_mapping[callback_query.data])
    await fill_deadline(callback_query, state)

async def fill_deadline(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Сколько дней осталось до сдачи работы?', reply_markup=deadline_diapason_kb)
    await state.set_state(DiplStates.deadline)

@router.callback_query(F.data.in_(['1-7days', '8-10days', '11-14days', '15days+']), StateFilter(DiplStates.deadline))
async def chosen_diapason_of_deadline(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    deadline_costing = {
        '1-7days': 10000,
         '8-10days': 9000,
         '11-14days': 8000,
         '15days+': 5000
    }
    deadline_mapping = {
        '1-7days': '1-7 дней',
         '8-10days': '8-10 дней',
         '11-14days': '11-14 дней',
         '15days+': '15+ дней'
    }
    TOTAL += deadline_costing[callback_query.data]
    await callback_query.message.answer(f'У вас осталось {deadline_mapping[callback_query.data]}')
    await state.update_data(deadline=deadline_mapping[callback_query.data])
    await fill_wishes(callback_query, state)

async def fill_wishes(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Есть ли у вас какие-то пожелания к работе?')
    await state.set_state(DiplStates.total)

"""
Проверка введённых данных
"""
# проверка на ̶в̶ш̶и̶в̶о̶с̶т̶ь̶  наличие текста
@router.message(StateFilter(DiplStates.theme), lambda x: x.text.isdigit())
async def warning_not_text(message: Message):
    await message.answer('Пожалуйста, введите тему вашей дипломной работы.')

# если в предыдущий хэндлер засунули что-то кроме оригинальности
@router.message(StateFilter(DiplStates.originality))
async def warning_not_originality(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для выбора процента оригинальности.')

# если в предыдущий хэндлер засунули что-то кроме дедлайна
@router.message(StateFilter(DiplStates.deadline))
async def warning_not_deadline(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для того чтобы указать сколько дней осталось до дедлайна,')   

"""
Тестовый возврат данных
"""
@router.message(StateFilter(DiplStates.total))
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
        f'Итоговая стоимость - {TOTAL}'
    )
    TOTAL = 0 