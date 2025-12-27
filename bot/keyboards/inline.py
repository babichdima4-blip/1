"""Inline keyboards."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_registration_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for experience selection during registration."""
    keyboard = [
        [InlineKeyboardButton(text="🆕 Новачок", callback_data="exp_newbie")],
        [InlineKeyboardButton(text="🎮 Маю досвід (1-5 ігор)", callback_data="exp_player")],
        [InlineKeyboardButton(text="⭐ Досвідчений (5+ ігор)", callback_data="exp_experienced")],
        [InlineKeyboardButton(text="🏆 Ветеран (багато ігор)", callback_data="exp_veteran")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for profile actions."""
    keyboard = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="profile_stats"),
            InlineKeyboardButton(text="🎖️ Ачівки", callback_data="profile_achievements")
        ],
        [
            InlineKeyboardButton(text="⚙️ Налаштування", callback_data="profile_settings"),
            InlineKeyboardButton(text="📜 Історія ігор", callback_data="profile_history")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_rating_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for rating views."""
    keyboard = [
        [
            InlineKeyboardButton(text="🏆 Топ-10", callback_data="rating_top10"),
            InlineKeyboardButton(text="📍 Моя позиція", callback_data="rating_my")
        ],
        [
            InlineKeyboardButton(text="👥 Команди", callback_data="rating_teams"),
            InlineKeyboardButton(text="📊 За категоріями", callback_data="rating_categories")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_schedule_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for schedule views."""
    keyboard = [
        [
            InlineKeyboardButton(text="📅 Найближчі", callback_data="schedule_upcoming"),
            InlineKeyboardButton(text="📋 Мої записи", callback_data="schedule_my")
        ],
        [
            InlineKeyboardButton(text="📜 Архів", callback_data="schedule_archive")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_achievements_keyboard() -> InlineKeyboardMarkup:
    """Get keyboard for achievements views."""
    keyboard = [
        [
            InlineKeyboardButton(text="📋 Всі", callback_data="achievements_all"),
            InlineKeyboardButton(text="✅ Завершені", callback_data="achievements_completed")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_achievement_detail_keyboard(achievement_id: int, is_claimed: bool = False) -> InlineKeyboardMarkup:
    """Get keyboard for achievement details."""
    keyboard = []

    if not is_claimed:
        keyboard.append([
            InlineKeyboardButton(
                text="🎁 Забрати нагороду",
                callback_data=f"claim_ach_{achievement_id}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="« Назад", callback_data="achievements_all")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
