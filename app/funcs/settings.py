import json
import os
import logging
from dotenv import load_dotenv
from app.settings.config import bot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SETTINGS_FILE = os.path.join(BASE_DIR, "app", "settings", "config.json")
ALERTS_DATA_FILE = os.path.join(BASE_DIR, "app", "settings", "alerts_data.json")

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.debug(f"BASE_DIR: {BASE_DIR}")


async def get_username(user_id):
    try:
        user = await bot.get_chat(user_id)
        if user.username:
            return f"@{user.username}"
        else:
            return str(user_id)
    except Exception as e:
        return f"Помилка: {e}"


def ensure_file_exists(file_path, default_content):
    """Проверяет, существует ли файл, и если нет – создает его с дефолтными значениями."""
    # Создаем родительскую директорию, если она отсутствует
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(default_content, file, ensure_ascii=False, indent=4)


def ensure_settings_file():
    """Создает файл настроек с дефолтными значениями, если он отсутствует."""
    default_settings = {"alert_text": "Тревога!", "calm_text": "Відбій!"}
    ensure_file_exists(SETTINGS_FILE, default_settings)


def read_alerts_data():
    """Считывает данные о тревогах из файла."""
    if not os.path.exists(ALERTS_DATA_FILE):
        return []

    with open(ALERTS_DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("alerts", [])


def read_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def write_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)


def get_setting(key, default=None):
    settings = read_settings()
    return settings.get(key, default)


def set_setting(key, value):
    settings = read_settings()
    settings[key] = value
    write_settings(settings)


def remove_setting(key):
    settings = read_settings()
    if key in settings:
        del settings[key]
        write_settings(settings)
