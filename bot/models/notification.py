"""Notification models."""
from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    """Notification model."""

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    # Type: achievement, rank_up, game_reminder, result, team, promo, admin
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    title: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    action_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    sent_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Notification U{self.user_id} {self.type}>"


class NotificationSettings(Base):
    """Notification settings for users."""

    __tablename__ = "notification_settings"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        primary_key=True
    )

    # Achievement notifications
    achievements: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    rank_up: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weekly_report: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Game notifications
    game_reminder_day: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    game_reminder_hour: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    game_results: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Team notifications
    team_messages: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    team_updates: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Shop and promo notifications
    shop_promos: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Admin notifications
    admin_announcements: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<NotificationSettings U{self.user_id}>"
