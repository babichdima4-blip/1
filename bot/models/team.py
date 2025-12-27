"""Team models."""
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


class Team(Base, TimestampMixin):
    """Team model."""

    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    tag: Mapped[Optional[str]] = mapped_column(String(10), unique=True, nullable=True)

    captain_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    vice_captain_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="SET NULL"),
        nullable=True
    )

    # Visual
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # HEX color
    logo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Settings
    max_members: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False
    )

    def __repr__(self) -> str:
        return f"<Team {self.name} [{self.tag}]>"


class TeamMember(Base, TimestampMixin):
    """Team member model."""

    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    # Role: captain, vice_captain, member
    role: Mapped[str] = mapped_column(String(20), default="member", nullable=False)

    # Preferred position: sniper, assault, support, sapper
    preferred_position: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    joined_at: Mapped[datetime] = mapped_column(nullable=False, server_default="now()")

    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="uq_team_member"),
    )

    def __repr__(self) -> str:
        return f"<TeamMember T{self.team_id} U{self.user_id} ({self.role})>"


class TeamStats(Base):
    """Team statistics for a season."""

    __tablename__ = "team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False
    )
    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False
    )

    games_played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    average_points: Mapped[Decimal] = mapped_column(
        Numeric(7, 2),
        default=0,
        nullable=False
    )
    rank_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("team_id", "season_id", name="uq_team_season_stats"),
    )

    def __repr__(self) -> str:
        return f"<TeamStats T{self.team_id} S{self.season_id}: {self.total_points}pts>"

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100
