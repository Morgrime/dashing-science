from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

support_keyboard = InlineKeyboardMarkup(inline_keyboard=[[ilnar_button], [danil_button], [vk_button]])

"""
Здесь будут кнопки для выбора услуги
"""

# курсовая
kurs_button = InlineKeyboardButton(
    text='Курсовая'
)

# диплом
diplom_button = InlineKeyboardButton(
    text='Диплом'
)

