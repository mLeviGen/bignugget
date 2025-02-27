BAD_ANSWER = "Ви не можете використовувати цю кнопку!"
CAPTION = "Виберіть дію:\n\nДля користувача: {}"
MAP = "app/images/map.png"

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


bot = Bot(token=TOKEN)
dp = Dispatcher()