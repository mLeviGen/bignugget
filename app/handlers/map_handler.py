import os
import logging
from aiogram import types, Router, Bot
from aiogram.types import FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from app.funcs import generate_map_image, get_username
from app.settings.config import CAPTION, BAD_ANSWER, MAP  
router = Router()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MAP = os.path.join(APP_DIR, "images", "map.png")

def get_map_image():
    return FSInputFile(MAP)

def set_keyboard(user_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Оновити", callback_data=f"refresh_map_{user_id}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data=f"back_to_menu_{user_id}")]
    ])

@router.callback_query(lambda c: c.data.startswith("show_map_"))
async def handle_show_map(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[-1])
    username = await get_username(user_id)
    if callback_query.from_user.id != user_id:
        await callback_query.answer(BAD_ANSWER, show_alert=True)
        return
    try:
        await generate_map_image()
        photo = get_map_image()
        media = InputMediaPhoto(media=photo, caption=f"Мапа тривог\n\nДля користувача: {username}")
        await callback_query.message.edit_media(media, reply_markup=set_keyboard(user_id))
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Помилка при обробці мапи: {e}")
        await callback_query.answer("Помилка обробки мапи.")

@router.callback_query(lambda c: c.data.startswith("refresh_map_"))
async def handle_refresh_map(callback_query: types.CallbackQuery, bot: Bot):
    user_id = int(callback_query.data.split("_")[-1])
    username = await get_username(user_id)
    if callback_query.from_user.id != user_id:
        await callback_query.answer(BAD_ANSWER, show_alert=True)
        return
    try:
        await callback_query.message.edit_caption("Оновляю мапу...")
        await generate_map_image()
        photo = get_map_image()
        media = InputMediaPhoto(media=photo, caption=f"Оновлена мапа\n\nДля користувача: {username}")
        await bot.edit_message_media(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            media=media,
            reply_markup=set_keyboard(user_id)
        )
        await callback_query.answer("Мапа оновлена!")
    except Exception as e:
        logging.error(f"Помилка при обробці мапи: {e}")
        await callback_query.answer("Помилка обробки мапи.")
