import os
import logging
from aiogram import types, Router
from aiogram.types import FSInputFile, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from app.funcs import read_alerts_data, get_username
from app.settings.config import CAPTION, BAD_ANSWER

router = Router()

# Текущая директория: .../app/handlers
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Поднимаемся на 2 уровня выше: .../app
APP_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))



# Путь к изображению: .../app/images/menus/nugget_alerts.png
image_alerts_path = os.path.join(APP_DIR, "images", "menus", "nugget_alerts.png")
logging.debug(f"[alerts_handler] CURRENT_DIR = {CURRENT_DIR}")
logging.debug(f"[alerts_handler] APP_DIR = {APP_DIR}")
logging.debug(f"[alerts_handler] Путь к изображению: {image_alerts_path}")
logging.debug(f"[alerts_handler] Файл существует? {os.path.exists(image_alerts_path)}")

image_alerts = FSInputFile(image_alerts_path)

@router.callback_query(lambda c: c.data.startswith("check_alert_"))
async def handle_check_alert(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split("_")[-1])
    username = await get_username(user_id)
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer(BAD_ANSWER, show_alert=True)
        return

    try:
        alerts_data = read_alerts_data()
        oblasts_under_alert = [
            alert["location_title"]
            for alert in alerts_data
            if alert.get("location_type") == "oblast"
        ]

        alert_message = (
            "Області з активною тривогою:\n" + "\n".join(oblasts_under_alert)
            if oblasts_under_alert
            else "Тривоги немає в областях."
        )
        back_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="⬅️ Назад", callback_data=f"back_to_menu_{user_id}"
                    )
                ]
            ]
        )
        media = InputMediaPhoto(
            media=image_alerts,
            caption=f"{alert_message}\n\nДля користувача: {username}",
        )
        await callback_query.message.edit_media(media, reply_markup=back_button)
        await callback_query.answer()
    except Exception as e:
        logging.error(f"Помилка при перевірці тривог: {e}")
        await callback_query.answer("Помилка при перевірці тривог.")
