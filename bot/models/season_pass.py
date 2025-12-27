"""Season pass models."""
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
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class SeasonPass(Base, TimestampMixin):
    """Season pass model."""

    __tablename__ = "season_passes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False
    )

    price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    games_included: Mapped[int] = mapped_column(Integer, nullable=False)
    point_multiplier: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=1.0,
        nullable=False
    )

    # perks: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<SeasonPass {self.name} (S{self.season_id})>"


class UserSeasonPass(Base, TimestampMixin):
    """User season pass model."""

    __tablename__ = "user_season_passes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    season_pass_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("season_passes.id", ondelete="CASCADE"),
        nullable=False
    )

    purchased_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default="now()"
    )
    games_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "season_pass_id", name="uq_user_season_pass"),
    )

    def __repr__(self) -> str:
        return f"<UserSeasonPass U{self.user_id} SP{self.season_pass_id}>"
