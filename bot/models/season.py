"""Season models."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Season(Base, TimestampMixin):
    """Season model representing a game season."""

    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    total_weeks: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    prize_pool: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)

    # Status: upcoming, active, completed
    status: Mapped[str] = mapped_column(String(20), default="upcoming", nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Season {self.number}: {self.name}>"


class SeasonRating(Base):
    """Season rating for each user in a season."""

    __tablename__ = "season_ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )

    # Stats
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wins: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    losses: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    mvp_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    missions_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    points_captured: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assists: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    kills: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deaths: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Streaks
    current_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    best_streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Position in leaderboard
    rank_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    last_game_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint("season_id", "user_id", name="uq_season_user"),
    )

    def __repr__(self) -> str:
        return f"<SeasonRating S{self.season_id} U{self.user_id}: {self.total_points}pts>"

    @property
    def win_rate(self) -> float:
        """Calculate win rate percentage."""
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100

    @property
    def kd_ratio(self) -> float:
        """Calculate K/D ratio."""
        if self.deaths == 0:
            return float(self.kills)
        return self.kills / self.deaths

    @property
    def average_points_per_game(self) -> float:
        """Calculate average points per game."""
        if self.games_played == 0:
            return 0.0
        return self.total_points / self.games_played
