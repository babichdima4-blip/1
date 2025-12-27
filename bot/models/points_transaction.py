"""Points transaction model."""
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class PointsTransaction(Base, TimestampMixin):
    """Points transaction model for tracking all point changes."""

    __tablename__ = "points_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Source type: game, achievement, reward, admin, referral, etc.
    source_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    source_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self) -> str:
        return f"<PointsTransaction U{self.user_id}: {self.amount:+d}pts>"
