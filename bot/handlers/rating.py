"""Rating handlers."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import get_rating_keyboard
from bot.models import User, Season, SeasonRating
from bot.services.user_service import get_user_by_telegram_id

router = Router(name="rating")


@router.message(Command("rating"))
@router.message(F.text == "🏆 Рейтинг")
async def cmd_rating(message: Message, session: AsyncSession):
    """Handle rating command."""
    await message.answer(
        "🏆 <b>РЕЙТИНГ</b>\n\n"
        "Обери, що хочеш переглянути:",
        reply_markup=get_rating_keyboard()
    )


@router.callback_query(F.data == "rating_top10")
async def show_top10_rating(callback: CallbackQuery, session: AsyncSession):
    """Show top 10 players."""
    # Get active season
    result = await session.execute(
        select(Season).where(Season.status == "active").limit(1)
    )
    season = result.scalar_one_or_none()

    if not season:
        await callback.answer(
            "📊 Рейтинг буде доступний після старту сезону!",
            show_alert=True
        )
        return

    # Get top 10 players in season
    result = await session.execute(
        select(SeasonRating, User)
        .join(User, SeasonRating.user_id == User.telegram_id)
        .where(SeasonRating.season_id == season.id)
        .order_by(desc(SeasonRating.total_points))
        .limit(10)
    )

    top_players = result.all()

    if not top_players:
        await callback.message.edit_text(
            "📊 Рейтинг поки порожній. Будь першим, хто зіграє!"
        )
        return

    # Format rating message
    rating_text = (
        f"🏆 <b>РЕЙТИНГ СЕЗОНУ {season.number}</b>\n"
        f"<i>{season.name}</i>\n\n"
    )

    medals = ["👑", "🥈", "🥉"]

    for idx, (rating, user) in enumerate(top_players, 1):
        medal = medals[idx - 1] if idx <= 3 else f"{idx}."
        win_rate = rating.win_rate
        rating_text += (
            f"{medal} <b>{user.nickname}</b>\n"
            f"   Очки: {rating.total_points} | "
            f"Ігор: {rating.games_played} | "
            f"W/L: {win_rate:.1f}%\n\n"
        )

    await callback.message.edit_text(rating_text)
    await callback.answer()


@router.callback_query(F.data == "rating_my")
async def show_my_rating(callback: CallbackQuery, session: AsyncSession):
    """Show user's position in rating."""
    user = await get_user_by_telegram_id(session, callback.from_user.id)

    if not user:
        await callback.answer("❌ Спочатку пройди реєстрацію!", show_alert=True)
        return

    # Get active season
    result = await session.execute(
        select(Season).where(Season.status == "active").limit(1)
    )
    season = result.scalar_one_or_none()

    if not season:
        await callback.answer(
            "📊 Рейтинг буде доступний після старту сезону!",
            show_alert=True
        )
        return

    # Get user's rating
    result = await session.execute(
        select(SeasonRating)
        .where(
            SeasonRating.season_id == season.id,
            SeasonRating.user_id == user.telegram_id
        )
    )
    user_rating = result.scalar_one_or_none()

    if not user_rating:
        await callback.message.edit_text(
            f"📍 <b>ТВОЯ ПОЗИЦІЯ</b>\n\n"
            f"Ти ще не брав участі в іграх цього сезону.\n\n"
            f"Зіграй першу гру, щоб з'явитися в рейтингу!"
        )
        return

    # Get total players count and user position
    result = await session.execute(
        select(SeasonRating.user_id)
        .where(SeasonRating.season_id == season.id)
        .order_by(desc(SeasonRating.total_points))
    )
    all_ratings = result.scalars().all()
    position = all_ratings.index(user.telegram_id) + 1 if user.telegram_id in all_ratings else None

    rating_text = (
        f"📍 <b>ТВОЯ ПОЗИЦІЯ</b>\n\n"
        f"Місце: #{position} з {len(all_ratings)}\n"
        f"Очки: {user_rating.total_points}\n\n"
        f"📊 Статистика:\n"
        f"Ігор зіграно: {user_rating.games_played}\n"
        f"Перемог: {user_rating.wins}\n"
        f"Поразок: {user_rating.losses}\n"
        f"Win Rate: {user_rating.win_rate:.1f}%\n"
        f"MVP: {user_rating.mvp_count} разів\n\n"
        f"🔥 Поточна серія: {user_rating.current_streak}\n"
        f"⭐ Найкраща серія: {user_rating.best_streak}"
    )

    await callback.message.edit_text(rating_text)
    await callback.answer()


@router.callback_query(F.data == "rating_teams")
async def show_teams_rating(callback: CallbackQuery):
    """Show teams rating."""
    # TODO: Implement teams rating
    await callback.answer("👥 Командний рейтинг в розробці!", show_alert=True)


@router.callback_query(F.data == "rating_categories")
async def show_categories_rating(callback: CallbackQuery):
    """Show rating by categories."""
    # TODO: Implement category ratings (best sniper, etc.)
    await callback.answer("📊 Рейтинг за категоріями в розробці!", show_alert=True)
