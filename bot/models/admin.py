"""Admin models."""
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class AdminRole(Base, TimestampMixin):
    """Admin role model."""

    __tablename__ = "admin_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    # Role: super_admin, organizer, moderator
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    # permissions: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    assigned_by: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
        nullable=True
    )

    def __repr__(self) -> str:
        return f"<AdminRole U{self.user_id}: {self.role}>"


class AdminLog(Base, TimestampMixin):
    """Admin action log model."""

    __tablename__ = "admin_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    action: Mapped[str] = mapped_column(String(50), nullable=False)
    target_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<AdminLog A{self.admin_id}: {self.action}>"
