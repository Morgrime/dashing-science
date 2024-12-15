import re

# Функция для проверки текста
def is_valid_text(text: str) -> bool:
    # Проверка, что текст не состоит только из цифр или из цифр и пробелов
    return not re.fullmatch(r'^\d+(\s*\d+)*$', text)