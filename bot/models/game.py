"""Game models."""
from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin


class Location(Base):
    """Location model for game venues."""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coordinates: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # facilities: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Location {self.name}>"


class Game(Base, TimestampMixin):
    """Game model."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=False
    )
    week_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Game type: regular, tournament, night, special, cqb
    game_type: Mapped[str] = mapped_column(String(20), default="regular", nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Schedule
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time_start: Mapped[time] = mapped_column(Time, nullable=False)
    time_end: Mapped[Optional[time]] = mapped_column(Time, nullable=True)

    location_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("locations.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Capacity
    max_players: Mapped[int] = mapped_column(Integer, default=40, nullable=False)

    # Price
    price: Mapped[Decimal] = mapped_column(Numeric(8, 2), nullable=False)
    price_with_season_pass: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(8, 2),
        nullable=True
    )

    # Points
    point_multiplier: Mapped[Decimal] = mapped_column(
        Numeric(3, 2),
        default=1.0,
        nullable=False
    )

    organizer_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="RESTRICT"),
        nullable=False
    )

    # Status: planned, registration_open, full, in_progress, completed, cancelled
    status: Mapped[str] = mapped_column(String(20), default="planned", nullable=False)

    weather: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f"<Game {self.title} on {self.date}>"

    @property
    def registered_count(self) -> int:
        """Get count of registered players (to be implemented with relationship)."""
        # This will be implemented with SQLAlchemy relationships
        return 0


class GameRegistration(Base, TimestampMixin):
    """Game registration model."""

    __tablename__ = "game_registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    team_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True
    )

    registered_at: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default="now()"
    )

    # Payment status: pending, paid, refunded
    payment_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False
    )
    payment_method: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    attended: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("game_id", "user_id", name="uq_game_user_registration"),
    )

    def __repr__(self) -> str:
        return f"<GameRegistration G{self.game_id} U{self.user_id}>"


class GameResult(Base, TimestampMixin):
    """Game result model."""

    __tablename__ = "game_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.telegram_id", ondelete="CASCADE"),
        nullable=False
    )
    team_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True
    )

    # Points
    points_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    base_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Results
    is_winner: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_mvp: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Stats
    kills: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deaths: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assists: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    points_captured: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    missions_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("game_id", "user_id", name="uq_game_user_result"),
    )

    def __repr__(self) -> str:
        return f"<GameResult G{self.game_id} U{self.user_id}: {self.points_earned}pts>"
