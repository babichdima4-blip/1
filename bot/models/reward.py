"""Reward models."""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Reward(Base, TimestampMixin):
    """Reward model."""

    __tablename__ = "rewards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Type: discount_code, free_game, merchandise, vip, custom
    type: Mapped[str] = mapped_column(String(20), nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    cost_points: Mapped[int] = mapped_column(Integer, nullable=False)

    discount_percent: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(3, 1),
        nullable=True
    )
    discount_amount: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 2),
        nullable=True
    )

    image_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stock: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Category: shop, games, merch, vip
    category: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    def __repr__(self) -> str:
        return f"<Reward {self.name} ({self.cost_points}pts)>"


class UserReward(Base, TimestampMixin):
    """User reward model."""

    __tablename__ = "user_rewards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    reward_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("rewards.id", ondelete="CASCADE"),
        nullable=False
    )

    promo_code: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True
    )

    claimed_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default="now()"
    )
    used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<UserReward U{self.user_id} R{self.reward_id}>"
