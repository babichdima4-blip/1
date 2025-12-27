"""User model."""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Date, String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model representing a player."""

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Experience level: newbie, player, experienced, veteran
    experience_level: Mapped[str] = mapped_column(
        String(20),
        default="newbie",
        nullable=False
    )

    # Points and rank
    total_historical_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_rank: Mapped[str] = mapped_column(String(20), default="newbie", nullable=False)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ban_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Profile
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Preferences stored as JSON
    # Example: {"notifications": {"games": true, "achievements": true}}
    # preferences: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    last_activity: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.nickname} (#{self.telegram_id})>"

    @property
    def full_name(self) -> str:
        """Get full name of the user."""
        return f"{self.first_name} {self.last_name}"
