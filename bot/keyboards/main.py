"""Main reply keyboard."""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    keyboard = [
        [
            KeyboardButton(text="👤 Мій профіль"),
            KeyboardButton(text="🏆 Рейтинг")
        ],
        [
            KeyboardButton(text="📅 Розклад"),
            KeyboardButton(text="👥 Команди")
        ],
        [
            KeyboardButton(text="🎖️ Ачівки"),
            KeyboardButton(text="🛒 Магазин")
        ],
        [
            KeyboardButton(text="❓ Допомога")
        ]
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Обери дію..."
    )
