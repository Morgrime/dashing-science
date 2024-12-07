from environs import Env

# api key
env = Env()
env.read_env()
BOT_TOKEN = env("TOKEN")
# ADMIN_IDS = env("ADMINS")