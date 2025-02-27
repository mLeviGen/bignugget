import os
import logging
from PIL import Image
from dotenv import load_dotenv
from alerts_in_ua import AsyncClient as AsyncAlertsClient
from app.funcs import read_alerts_data

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

MAP = os.path.join(APP_DIR, "app", "images", "map.png")
UKRAINE = os.path.join(APP_DIR, "app", "images", "UK2.png")
CITIES = os.path.join(APP_DIR, "app", "images", "cities")

load_dotenv()
TOKEN = os.getenv("ALERTS_IN_UA_TOKEN")
logger = logging.getLogger(__name__)

async def get_alerts():
    try:
        alerts_client = AsyncAlertsClient(TOKEN)
        active_alerts = await alerts_client.get_active_alerts()
        logger.debug("Данные о тревогах успешно получены")
        return active_alerts
    except Exception as e:
        logger.error(f"Помилка отримання тривог: {e}")
        raise

async def generate_map_image():
    try:
        logger.debug("Начало генерации карты")

        def filter_oblasts(alerts):
            return [alert["location_title"] for alert in alerts if alert.get("location_type") == "oblast"]

        alerts_data = read_alerts_data()
        if not isinstance(alerts_data, list):
            logger.error("Невірний формат: очікувався список.")
            raise ValueError("Невірний формат: очікувався список.")

        active_oblasts = filter_oblasts(alerts_data)
        logger.debug(f"Знайдені області з тривогою: {active_oblasts}")

        oblast_map = {
            "Сумська область": 1,
            "Чернігівська область": 2,
            "Київська область": 3,
            "Житомирська область": 4,
            "Рівненська область": 5,
            "Волинська область": 6,
            "Львівська область": 7,
            "Закарпатська область": 8,
            "Івано-Франківська область": 9,
            "Тернопільська область": 10,
            "Чернівецька область": 11,
            "Хмельницька область": 12,
            "Вінницька область": 13,
            "Одеська область": 14,
            "Черкаська область": 15,
            "Кіровоградська область": 16,
            "Миколаївська область": 17,
            "Полтавська область": 18,
            "Харківська область": 19,
            "Луганська область": 20,
            "Дніпропетровська область": 21,
            "Донецька область": 22,
            "Запорізька область": 23,
            "Херсонська область": 24,
            "Автономна Республіка Крим": 25,
        }

        active_ids = [oblast_map[obl] for obl in active_oblasts if obl in oblast_map]
        logger.debug(f"ID активних областей: {active_ids}")

        def create_mask(active_list, size):
            img = Image.new("RGBA", size, (255, 255, 255, 0))
            for id_ in active_list:
                mask_path = os.path.join(CITIES, f"{id_}.png")
                if not os.path.exists(mask_path):
                    logger.error(f"Файл маски не найден: {mask_path}")
                    continue
                mask = Image.open(mask_path).convert("RGBA")
                img.paste(mask, (0, 0), mask)
            return img

        if not os.path.exists(UKRAINE):
            logger.error("Файл базової карти не знайдено")
            raise FileNotFoundError("UK2.png не знайдено")

        base_image = Image.open(UKRAINE).convert("RGBA")
        size = base_image.size
        mask_image = create_mask(active_ids, size) 
        overlay = Image.new("RGBA", size, (235, 76, 66))
        base_image.paste(overlay, (0, 0), mask_image)
        final_image = Image.new("RGBA", (size[0] + 100, size[1] + 100), (49, 51, 64))
        final_image.paste(base_image, (50, 50))
        final_image.save(MAP)
        logger.debug("Карта збережена успішно!")
    except Exception as e:
        logger.error(f"Помилка в generate_map_image: {e}")
        raise
