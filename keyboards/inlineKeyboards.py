from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ilnar_button = InlineKeyboardButton(
    text='Поддержка пользователя',
    url='https://t.me/yeltler'
)

danil_button = InlineKeyboardButton(
    text='Техподдержка',
    url='https://t.me/Morgrime'
)

vk_button = InlineKeyboardButton(
    text='Группа ВК',
    url='https://vk.com/lihaya_nauka'
)


support_keyboard = InlineKeyboardMarkup(inline_keyboard=[[ilnar_button], [danil_button], [vk_button]])