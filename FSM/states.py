from aiogram.fsm.state import State, StatesGroup

class Universal(StatesGroup):
    choice = State()

class KursStates(StatesGroup):
    theme = State() # вопрос какая тема
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)
    total = State() # вывод заполненной информации

class DiplStates(StatesGroup):
    theme = State() 
    project = State() # проектная вкр или нет
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)
    total = State()

class RefStates(StatesGroup):
    theme = State()
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)
    total = State()

class ScienceStates(StatesGroup):
    theme = State()
    originality = State() # какой процент оригинальности нужен
    deadline = State() # сколько дней до дедлайна
    wishes = State() # пожелания (не обязательно)
    total = State()