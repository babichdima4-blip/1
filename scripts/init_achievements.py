"""Script to initialize basic achievements in the database."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from bot.database import async_session_maker
from bot.models import Achievement


async def init_achievements():
    """Initialize basic 10 achievements."""
    achievements_data = [
        # Activity achievements
        {
            "code": "first_game",
            "category": "activity",
            "name": "Перші кроки",
            "description": "Зіграти першу гру",
            "icon": "🎯",
            "condition_type": "counter",
            "reward_points": 10,
            "difficulty": 1,
            "is_hidden": False,
        },
        {
            "code": "games_5",
            "category": "activity",
            "name": "Активний гравець",
            "description": "Зіграти 5 ігор",
            "icon": "🔥",
            "condition_type": "counter",
            "reward_points": 30,
            "difficulty": 2,
            "is_hidden": False,
        },
        {
            "code": "games_10",
            "category": "activity",
            "name": "Ветеран",
            "description": "Зіграти 10 ігор",
            "icon": "⭐",
            "condition_type": "counter",
            "reward_points": 50,
            "difficulty": 3,
            "is_hidden": False,
        },
        # Victory achievements
        {
            "code": "first_win",
            "category": "victories",
            "name": "Перша перемога",
            "description": "Виграти першу гру",
            "icon": "🏆",
            "condition_type": "counter",
            "reward_points": 15,
            "difficulty": 1,
            "is_hidden": False,
        },
        {
            "code": "win_streak_3",
            "category": "victories",
            "name": "Серія переможця",
            "description": "Виграти 3 гри підряд",
            "icon": "🔥",
            "condition_type": "counter",
            "reward_points": 40,
            "difficulty": 3,
            "is_hidden": False,
        },
        # MVP achievements
        {
            "code": "first_mvp",
            "category": "mastery",
            "name": "Зірка матчу",
            "description": "Отримати звання MVP",
            "icon": "⭐",
            "condition_type": "counter",
            "reward_points": 25,
            "difficulty": 2,
            "is_hidden": False,
        },
        {
            "code": "mvp_3",
            "category": "mastery",
            "name": "Легенда поля",
            "description": "Отримати MVP 3 рази",
            "icon": "👑",
            "condition_type": "counter",
            "reward_points": 60,
            "difficulty": 4,
            "is_hidden": False,
        },
        # Team achievements
        {
            "code": "join_team",
            "category": "team",
            "name": "Командний гравець",
            "description": "Приєднатися до команди",
            "icon": "👥",
            "condition_type": "boolean",
            "reward_points": 20,
            "difficulty": 1,
            "is_hidden": False,
        },
        {
            "code": "team_captain",
            "category": "team",
            "name": "Лідер",
            "description": "Стати капітаном команди",
            "icon": "🎖️",
            "condition_type": "boolean",
            "reward_points": 50,
            "difficulty": 3,
            "is_hidden": False,
        },
        # Hidden achievement
        {
            "code": "early_bird",
            "category": "hidden",
            "name": "Рання пташка",
            "description": "Зареєструватися в перших 100 гравців",
            "icon": "🐦",
            "condition_type": "custom",
            "reward_points": 100,
            "difficulty": 5,
            "is_hidden": True,
        },
    ]

    async with async_session_maker() as session:
        for ach_data in achievements_data:
            # Check if achievement already exists
            result = await session.execute(
                select(Achievement).where(Achievement.code == ach_data["code"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"✓ Achievement '{ach_data['code']}' already exists, skipping...")
                continue

            # Create achievement
            achievement = Achievement(**ach_data)
            session.add(achievement)
            print(f"+ Created achievement: {ach_data['name']} ({ach_data['code']})")

        await session.commit()
        print(f"\n✅ Successfully initialized {len(achievements_data)} achievements!")


if __name__ == "__main__":
    print("🎖️  Initializing achievements...\n")
    asyncio.run(init_achievements())
