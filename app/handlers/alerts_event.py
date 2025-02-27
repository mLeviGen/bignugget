from datetime import datetime, timezone
import json
import logging
import asyncio
from app.funcs.alerts import get_alerts
from app.funcs import ALERTS_DATA_FILE


def custom_serializer(obj):
    """Серіалізатор для об'єктів, що не підтримуються JSON."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


async def update_alerts_data():
    """Фонова задача для оновлення информації про тривогу кожні 6 секунд (ліміт API)."""
    while True:
        try:
            alerts_data = await get_alerts()
            with open(ALERTS_DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "alerts": [alert.__dict__ for alert in alerts_data],
                    },
                    file,
                    ensure_ascii=False,
                    indent=4,
                    default=custom_serializer,
                )
            logging.info("Дані тривог успішно оновлені й збережені.")
        except TypeError as te:
            logging.error(f"Помилка при сериализації даних: {te}")
        except Exception as e:
            logging.error(f"Помилка оновлення інформації: {e}")

        await asyncio.sleep(7)
