import asyncio
import logging
from app import setup_routes
from app.handlers.alerts_event import update_alerts_data
from app.funcs import ensure_settings_file
from app.settings.config import bot, dp

logging.basicConfig(level=logging.DEBUG)


async def main():
    try:
        logging.info("Запуск бота...")
        asyncio.create_task(update_alerts_data())
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Критична помилка: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    setup_routes(dp)
    ensure_settings_file()

    asyncio.run(main())
