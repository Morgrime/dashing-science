from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

"""
Функциональные кнопки
"""
cancel_button = InlineKeyboardButton(
    text='Отмена',
    callback_data='cancel_button'
)

cancel_kb = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])

yes_button = InlineKeyboardButton(
    text='Да',
    callback_data='yes_button'
)

no_button = InlineKeyboardButton(
    text='Нет',
    callback_data='no_button'
)

yes_no_kb = InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button], [cancel_button]])

"""
Здесь будут кнопки для связи с техподдержкой
"""
# ссылка на ильнара
ilnar_button = InlineKeyboardButton(
    text='Поддержка пользователя',
    url='https://t.me/yeltler'
)

# ссылка на меня (создателя бота)
danil_button = InlineKeyboardButton(
    text='Техподдержка',
    url='https://t.me/Morgrime'
)

# ссылка на группу вк 
vk_button = InlineKeyboardButton(
    text='Группа ВК',
    url='https://vk.com/lihaya_nauka'
)

support_kb = InlineKeyboardMarkup(inline_keyboard=[[ilnar_button, danil_button, vk_button], [cancel_button]])


"""
Здесь будут кнопки для выбора услуги
"""

# курсовая
kurs_button = InlineKeyboardButton(
    text='Курсовая',
    callback_data='kurs_button'
)

# диплом
diplom_button = InlineKeyboardButton(
    text='Диплом',
    callback_data='dipl_button'
)

# реферат
ref_button = InlineKeyboardButton(
    text='Реферат',
    callback_data='ref_button'
)

# научная статья
science_button = InlineKeyboardButton(
    text='Науч. статья',
    callback_data='science_button'
)

service_kb = InlineKeyboardMarkup(inline_keyboard=[[kurs_button, diplom_button, ref_button, science_button], [cancel_button]])


"""
Диапазоны оригинальности
"""
fifty = InlineKeyboardButton(
    text='50%+',
    callback_data='fifty'
)

sixty = InlineKeyboardButton(
    text='60%+',
    callback_data='sixty'
)

seventy = InlineKeyboardButton(
    text='70%+',
    callback_data='seventy'
)

eighty = InlineKeyboardButton(
    text='80%+',
    callback_data='eighty'
)

ninety_plus = InlineKeyboardButton(
    text='90%+',
    callback_data='ninety'
)

originality_diapason_kb = InlineKeyboardMarkup(inline_keyboard=[[fifty, sixty, seventy, 
                                                                 eighty, ninety_plus], [cancel_button]])


"""
Диапазоны дедлайна
"""
one_to_three = InlineKeyboardButton(
    text='1-3 дней',
    callback_data='1-3days'
)

four_to_seven = InlineKeyboardButton(
    text='4-7 дней',
    callback_data='4-7days'
)

eight_to_ten = InlineKeyboardButton(
    text='8-10 дней',
    callback_data='8-10days'
)

eleven_to_14 = InlineKeyboardButton(
    text='11-14 дней',
    callback_data='11-14days'
)

two_week_plus = InlineKeyboardButton(
    text='15+ дней',
    callback_data='15days+'
)

deadline_diapason_kb = InlineKeyboardMarkup(inline_keyboard=[[one_to_three, four_to_seven, eight_to_ten, 
                                                              eleven_to_14, two_week_plus], [cancel_button]])