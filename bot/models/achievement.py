"""Achievement models."""
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Achievement(Base, TimestampMixin):
    """Achievement model."""

    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Category: activity, victories, mastery, team, events, shop, hidden
    category: Mapped[str] = mapped_column(String(20), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)

    # Condition type: counter, boolean, date, custom
    condition_type: Mapped[str] = mapped_column(String(20), nullable=False)
    # condition_value: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Rewards
    reward_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reward_discount: Mapped[Optional[float]] = mapped_column(Numeric(3, 1), nullable=True)
    # reward_items: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Metadata
    difficulty: Mapped[int] = mapped_column(Integer, default=1, nullable=False)  # 1-5
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_seasonal: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    season_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=True
    )

    available_from: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    available_to: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Achievement {self.code}: {self.name}>"


class UserAchievement(Base):
    """User achievement progress model."""

    __tablename__ = "user_achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    achievement_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("achievements.id", ondelete="CASCADE"),
        nullable=False
    )

    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    claimed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )

    def __repr__(self) -> str:
        return f"<UserAchievement U{self.user_id} A{self.achievement_id}: {self.progress}>"
