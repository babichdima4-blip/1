"""Achievement service for managing achievements and checking conditions."""
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import (
    Achievement,
    UserAchievement,
    User,
    SeasonRating,
    GameResult,
    Team,
    TeamMember,
)


async def get_all_achievements(session: AsyncSession) -> List[Achievement]:
    """Get all achievements."""
    result = await session.execute(
        select(Achievement).order_by(Achievement.category, Achievement.difficulty)
    )
    return result.scalars().all()


async def get_user_achievements(
    session: AsyncSession,
    user_id: int,
    completed_only: bool = False
) -> List[tuple[UserAchievement, Achievement]]:
    """Get user's achievements with their details."""
    query = (
        select(UserAchievement, Achievement)
        .join(Achievement, UserAchievement.achievement_id == Achievement.id)
        .where(UserAchievement.user_id == user_id)
    )

    if completed_only:
        query = query.where(UserAchievement.is_completed == True)

    result = await session.execute(query.order_by(Achievement.category))
    return result.all()


async def get_or_create_user_achievement(
    session: AsyncSession,
    user_id: int,
    achievement_id: int
) -> UserAchievement:
    """Get or create user achievement record."""
    result = await session.execute(
        select(UserAchievement).where(
            and_(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id
            )
        )
    )
    user_achievement = result.scalar_one_or_none()

    if not user_achievement:
        user_achievement = UserAchievement(
            user_id=user_id,
            achievement_id=achievement_id,
            progress=0,
            is_completed=False,
            claimed=False
        )
        session.add(user_achievement)
        await session.flush()

    return user_achievement


async def update_achievement_progress(
    session: AsyncSession,
    user_id: int,
    achievement_code: str,
    progress: int
) -> Optional[UserAchievement]:
    """Update progress for a specific achievement."""
    # Get achievement
    result = await session.execute(
        select(Achievement).where(Achievement.code == achievement_code)
    )
    achievement = result.scalar_one_or_none()

    if not achievement:
        return None

    # Get or create user achievement
    user_achievement = await get_or_create_user_achievement(
        session, user_id, achievement.id
    )

    # Update progress
    user_achievement.progress = progress

    # Check if completed
    if not user_achievement.is_completed:
        # Check completion based on condition type
        if achievement.condition_type == "counter":
            # For counter achievements, check if progress >= target
            # Target is stored in condition_value (we'll parse it later)
            target = 1  # Default
            if progress >= target:
                user_achievement.is_completed = True
                user_achievement.completed_at = datetime.utcnow()

    await session.flush()
    return user_achievement


async def check_and_update_achievements(
    session: AsyncSession,
    user_id: int,
    event_type: str
) -> List[UserAchievement]:
    """Check and update achievements based on event type."""
    newly_completed = []

    if event_type == "game_completed":
        # Check game-related achievements
        newly_completed.extend(
            await _check_game_achievements(session, user_id)
        )
    elif event_type == "team_joined":
        # Check team-related achievements
        newly_completed.extend(
            await _check_team_achievements(session, user_id)
        )

    return newly_completed


async def _check_game_achievements(
    session: AsyncSession,
    user_id: int
) -> List[UserAchievement]:
    """Check game-related achievements."""
    newly_completed = []

    # Get user's game statistics
    result = await session.execute(
        select(func.count(GameResult.id))
        .where(GameResult.user_id == user_id)
    )
    total_games = result.scalar() or 0

    # Achievement: "first_game" - Play first game
    if total_games >= 1:
        ua = await update_achievement_progress(
            session, user_id, "first_game", total_games
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    # Achievement: "games_5" - Play 5 games
    if total_games >= 5:
        ua = await update_achievement_progress(
            session, user_id, "games_5", total_games
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    # Achievement: "games_10" - Play 10 games
    if total_games >= 10:
        ua = await update_achievement_progress(
            session, user_id, "games_10", total_games
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    # Check win streak
    result = await session.execute(
        select(SeasonRating.current_streak)
        .where(SeasonRating.user_id == user_id)
        .order_by(SeasonRating.current_streak.desc())
        .limit(1)
    )
    max_streak = result.scalar() or 0

    if max_streak >= 3:
        ua = await update_achievement_progress(
            session, user_id, "win_streak_3", max_streak
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    # Check MVP count
    result = await session.execute(
        select(func.count(GameResult.id))
        .where(
            and_(
                GameResult.user_id == user_id,
                GameResult.is_mvp == True
            )
        )
    )
    mvp_count = result.scalar() or 0

    if mvp_count >= 1:
        ua = await update_achievement_progress(
            session, user_id, "first_mvp", mvp_count
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    if mvp_count >= 3:
        ua = await update_achievement_progress(
            session, user_id, "mvp_3", mvp_count
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

    return newly_completed


async def _check_team_achievements(
    session: AsyncSession,
    user_id: int
) -> List[UserAchievement]:
    """Check team-related achievements."""
    newly_completed = []

    # Check if user is in a team
    result = await session.execute(
        select(TeamMember)
        .where(TeamMember.user_id == user_id)
    )
    team_membership = result.scalar_one_or_none()

    if team_membership:
        ua = await update_achievement_progress(
            session, user_id, "join_team", 1
        )
        if ua and ua.is_completed and not ua.claimed:
            newly_completed.append(ua)

        # Check if captain
        result = await session.execute(
            select(Team).where(Team.captain_id == user_id)
        )
        is_captain = result.scalar_one_or_none() is not None

        if is_captain:
            ua = await update_achievement_progress(
                session, user_id, "team_captain", 1
            )
            if ua and ua.is_completed and not ua.claimed:
                newly_completed.append(ua)

    return newly_completed


async def claim_achievement_rewards(
    session: AsyncSession,
    user_id: int,
    achievement_id: int
) -> bool:
    """Claim rewards for completed achievement."""
    result = await session.execute(
        select(UserAchievement, Achievement)
        .join(Achievement)
        .where(
            and_(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement_id,
                UserAchievement.is_completed == True,
                UserAchievement.claimed == False
            )
        )
    )

    row = result.first()
    if not row:
        return False

    user_achievement, achievement = row

    # Mark as claimed
    user_achievement.claimed = True

    # Add points to user if any
    if achievement.reward_points > 0:
        from bot.services.user_service import add_points_to_user
        await add_points_to_user(session, user_id, achievement.reward_points)

    await session.flush()
    return True


async def get_achievement_stats(
    session: AsyncSession,
    user_id: int
) -> dict:
    """Get user's achievement statistics."""
    # Total achievements
    result = await session.execute(
        select(func.count(Achievement.id))
    )
    total_achievements = result.scalar() or 0

    # Completed achievements
    result = await session.execute(
        select(func.count(UserAchievement.id))
        .where(
            and_(
                UserAchievement.user_id == user_id,
                UserAchievement.is_completed == True
            )
        )
    )
    completed_count = result.scalar() or 0

    # Completion percentage
    completion_percentage = (
        (completed_count / total_achievements * 100)
        if total_achievements > 0
        else 0
    )

    return {
        "total": total_achievements,
        "completed": completed_count,
        "percentage": round(completion_percentage, 1)
    }
