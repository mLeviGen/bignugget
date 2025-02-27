from aiogram import Dispatcher
from .handlers import (
    menu_handler,
    map_handler,
    alert_handler,
)

__all__ = [
    "menu_handler",
    "map_handler",
    "alert_handler",
]


def setup_routes(dp: Dispatcher):
    dp.include_router(menu_handler.router)
    dp.include_router(map_handler.router)
    dp.include_router(alert_handler.router)
