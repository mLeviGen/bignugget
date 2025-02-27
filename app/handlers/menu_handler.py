import os
import logging
from aiogram import Bot, types, Router
from aiogram.types import FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from app.settings.config import CAPTION, BAD_ANSWER, bot
from app.funcs import get_username

router = Router()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

image_main_path = os.path.join(APP_DIR, "app", "images", "menus", "nugget.png")

try:
    file_obj = open(image_main_path, "rb")
except Exception as e:
    logging.error(f"Ошибка открытия файла: {e}")
    raise

def get_image_main():
    return FSInputFile(image_main_path)

image_main = FSInputFile(file_obj, filename=os.path.basename(image_main_path))

logging.debug(f"[main_menu_handler] CURRENT_DIR = {CURRENT_DIR}")
logging.debug(f"[main_menu_handler] APP_DIR = {APP_DIR}")
logging.debug(f"[main_menu_handler] Путь к изображению: {image_main_path}")
logging.debug(f"[main_menu_handler] Файл существует? {os.path.exists(image_main_path)}")


def set_keyboard(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗺️ Карта", callback_data=f"show_map_{user_id}")],
            [InlineKeyboardButton(text="🚨 Тривога", callback_data=f"check_alert_{user_id}")]
        ]
    )

async def show_main_menu(bot: Bot, chat_id: int, user_id: int):
    username = await get_username(user_id)
    try:
        await bot.send_photo(
            chat_id,
            get_image_main(),
            caption=CAPTION.format(username),
            reply_markup=set_keyboard(user_id),
        )
    except Exception as e:
        logging.error(f"Помилка відправлення головного меню: {e}")


@router.message(Command(commands=["menu"]))
async def show_menu(message: types.Message, bot: Bot):
    await show_main_menu(bot, message.chat.id, message.from_user.id)

@router.message(Command(commands=["start"]))
async def start_command(message: types.Message, bot: Bot):
    await show_main_menu(bot, message.chat.id, message.from_user.id)

@router.callback_query(lambda c: c.data.startswith("back_to_menu_"))
async def handle_back_to_menu(callback_query: types.CallbackQuery, bot: Bot):
    user_id = int(callback_query.data.split("_")[-1])
    username = await get_username(user_id)

    if callback_query.from_user.id != user_id:
        await callback_query.answer(BAD_ANSWER, show_alert=True)
        return

    try:
        media = InputMediaPhoto(
            media=get_image_main(),
            caption=CAPTION.format(username),
        )
        await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=media,
            reply_markup=set_keyboard(user_id),
        )
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Помилка відправлення головного меню: {e}")
        await callback_query.answer("Помилка відправлення головного меню.")

