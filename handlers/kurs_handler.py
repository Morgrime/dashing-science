from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from FSM.states import KursStates
from keyboards.inlineKeyboards import cancel_kb, originality_diapason_kb, deadline_diapason_kb

router = Router()

user_dict: dict[int, dict[str, str | int | bool]] = {}
TOTAL = 0

"""
Курсовая - хэдлер для начала рассчета стоимости курсовой
"""
# вопрос про тему
@router.callback_query(lambda c: c.data == 'kurs_button', StateFilter(default_state))    
async def choose_kurs(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    TOTAL += 3000
    await callback_query.message.answer('Вы выбрали курсовую, пожалуйста ответьте на несколько вопросов, чтобы мы могли оценить вашу работу\n')
    await fill_theme(callback_query, state)

async def fill_theme(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Напишите тему вашей курсовой работы.', reply_markup=cancel_kb)
    await state.set_state(KursStates.theme) # установления состояния "Тема"

# вопрос про процент оригинальности
@router.message(StateFilter(KursStates.theme), F.text.isalpha())    
async def fill_originality(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer('Какой процент оригинальности вы ожидаете?\n', 
                         reply_markup=originality_diapason_kb)
    await state.set_state(KursStates.originality) # установление состояния "Оригинальность"

# выбор диапазона оригинальности
@router.callback_query(F.data.in_(['sixty', 'seventy', 'eighty', 'ninety']), StateFilter(KursStates.originality))
async def choosen_diapason_of_originality(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    originality_costing = {
        'sixty': 300,
        'seventy': 450,
        'eighty': 750,
        'ninety': 1050
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
    await state.set_state(KursStates.deadline)

@router.callback_query(F.data.in_(['1-7days', '8-10days', '11-14days', '15days+']), StateFilter(KursStates.deadline))
async def chosen_diapason_of_deadline(callback_query: types.CallbackQuery, state: FSMContext):
    global TOTAL
    deadline_costing = {
        '1-7days': 1500,
         '8-10days': 900,
         '11-14days': 450,
         '15days+': 0
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
    await state.set_state(KursStates.total)

"""
Проверка введённых данных
"""
# проверка на ̶в̶ш̶и̶в̶о̶с̶т̶ь̶  наличие текста
@router.message(StateFilter(KursStates.theme), lambda x: x.text.isdigit())
async def warning_not_text(message: Message):
    await message.answer('Пожалуйста, введите тему вашей курсовой.')

# если в предыдущий хэндлер засунули что-то кроме оригинальности
@router.message(StateFilter(KursStates.originality))
async def warning_not_originality(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для выбора процента оригинальности.')

# если в предыдущий хэндлер засунули что-то кроме дедлайна
@router.message(StateFilter(KursStates.deadline))
async def warning_not_deadline(message: Message):
    await message.answer('Пожалуйста, используйте кнопки для того чтобы указать сколько дней осталось до дедлайна,')   

"""
Тестовый возврат данных
"""
@router.message(StateFilter(KursStates.total))
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