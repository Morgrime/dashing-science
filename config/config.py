from environs import Env

# api key
env = Env()
env.read_env()
BOT_TOKEN = env("TOKEN")
# DB_NAME = env("DB_NAME")  # Имя базы данных
# DB_USER = env("DB_USER")  # Имя пользователя
# DB_PASS = env("DB_PASS") # Пароль
# DB_HOST = env("DB_HOST")  # Хост сервера PostgreSQL
# DB_PORT = env("DB_PORT")  # Порт сервера PostgreSQL
