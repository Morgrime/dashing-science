# Используем легкий образ Alpine Linux с предустановленным Python 3.12.6
FROM python:3.12.6-alpine

# Обновляем репозитории и устанавливаем зависимости
RUN apk update && apk add --no-cache gcc musl-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Указываем команду для запуска бота
CMD ["python", "main.py"]
