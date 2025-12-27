"""Handlers package."""
from aiogram import Dispatcher

from . import start, profile, rating, schedule, achievements


def register_all_handlers(dp: Dispatcher):
    """Register all bot handlers."""
    # Register routers in order of priority
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(rating.router)
    dp.include_router(schedule.router)
    dp.include_router(achievements.router)
