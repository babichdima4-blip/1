"""Application settings and configuration."""
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# Telegram Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS: List[int] = [int(id_) for id_ in os.getenv("ADMIN_IDS", "").split(",") if id_]

# Database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "airsoft_bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Database URL
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SYNC_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Admin Panel settings
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "dev-secret-key-change-in-production")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

# Application settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# External APIs
LIQPAY_PUBLIC_KEY = os.getenv("LIQPAY_PUBLIC_KEY", "")
LIQPAY_PRIVATE_KEY = os.getenv("LIQPAY_PRIVATE_KEY", "")
MONOBANK_TOKEN = os.getenv("MONOBANK_TOKEN", "")

# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

# Game settings
DEFAULT_POINTS_FOR_PARTICIPATION = 10
DEFAULT_POINTS_FOR_WIN = 5
DEFAULT_POINTS_FOR_MISSION = 3
DEFAULT_POINTS_FOR_MVP = 5
DEFAULT_POINTS_FOR_ASSIST = 2
DEFAULT_POINTS_FOR_POINT_CAPTURE = 2

# Point multipliers by day of week (0=Monday, 6=Sunday)
DAY_MULTIPLIERS = {
    0: 0.7,  # Monday
    1: 0.7,  # Tuesday
    2: 0.7,  # Wednesday
    3: 0.7,  # Thursday
    4: 0.7,  # Friday
    5: 1.0,  # Saturday
    6: 1.2,  # Sunday
}

# Game type multipliers
GAME_TYPE_MULTIPLIERS = {
    "regular": 1.0,
    "tournament": 1.5,
    "night": 1.3,
    "special": 1.4,
    "cqb": 1.2,
}

# Rank thresholds
RANK_THRESHOLDS = {
    "newbie": 0,
    "player": 200,
    "experienced": 500,
    "veteran": 1000,
    "legend": 2000,
}

# Season settings
DEFAULT_SEASON_WEEKS = 12
