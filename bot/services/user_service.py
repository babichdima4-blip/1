"""User service for database operations."""
from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import User
from config import RANK_THRESHOLDS


async def get_user_by_telegram_id(
    session: AsyncSession,
    telegram_id: int
) -> Optional[User]:
    """Get user by telegram ID."""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str,
    nickname: str,
    phone: Optional[str] = None,
    experience_level: str = "newbie"
) -> User:
    """Create a new user."""
    user = User(
        telegram_id=telegram_id,
        first_name=first_name,
        last_name=last_name,
        nickname=nickname,
        phone=phone,
        experience_level=experience_level,
        current_rank="newbie",
        total_historical_points=0,
        is_active=True,
        last_activity=datetime.utcnow()
    )

    session.add(user)
    await session.flush()
    return user


async def update_user_rank(session: AsyncSession, user: User) -> bool:
    """Update user rank based on total points. Returns True if rank changed."""
    old_rank = user.current_rank
    new_rank = "newbie"

    # Determine rank based on total points
    for rank, threshold in sorted(RANK_THRESHOLDS.items(), key=lambda x: x[1], reverse=True):
        if user.total_historical_points >= threshold:
            new_rank = rank
            break

    if old_rank != new_rank:
        user.current_rank = new_rank
        await session.flush()
        return True

    return False


async def add_points_to_user(
    session: AsyncSession,
    user_id: int,
    points: int
) -> User:
    """Add points to user's total."""
    await session.execute(
        update(User)
        .where(User.telegram_id == user_id)
        .values(total_historical_points=User.total_historical_points + points)
    )

    await session.flush()

    # Get updated user
    user = await get_user_by_telegram_id(session, user_id)
    await update_user_rank(session, user)

    return user


async def update_last_activity(session: AsyncSession, user_id: int):
    """Update user's last activity timestamp."""
    await session.execute(
        update(User)
        .where(User.telegram_id == user_id)
        .values(last_activity=datetime.utcnow())
    )
