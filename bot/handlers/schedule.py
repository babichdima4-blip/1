"""Schedule handlers."""
from datetime import datetime, date
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import get_schedule_keyboard
from bot.models import Game, Location, GameRegistration
from bot.services.user_service import get_user_by_telegram_id

router = Router(name="schedule")


@router.message(Command("schedule"))
@router.message(F.text == "📅 Розклад")
async def cmd_schedule(message: Message):
    """Handle schedule command."""
    await message.answer(
        "📅 <b>РОЗКЛАД ІГОР</b>\n\n"
        "Обери, що хочеш переглянути:",
        reply_markup=get_schedule_keyboard()
    )


@router.callback_query(F.data == "schedule_upcoming")
async def show_upcoming_games(callback: CallbackQuery, session: AsyncSession):
    """Show upcoming games."""
    # Get upcoming games
    today = date.today()

    result = await session.execute(
        select(Game, Location)
        .join(Location, Game.location_id == Location.id)
        .where(
            and_(
                Game.date >= today,
                Game.status.in_(["planned", "registration_open"])
            )
        )
        .order_by(Game.date, Game.time_start)
        .limit(5)
    )

    games = result.all()

    if not games:
        await callback.message.edit_text(
            "📅 Наразі немає запланованих ігор.\n"
            "Слідкуй за оновленнями!"
        )
        return

    schedule_text = "📅 <b>НАЙБЛИЖЧІ ІГРИ:</b>\n\n"

    for game, location in games:
        # Get registrations count
        reg_result = await session.execute(
            select(GameRegistration.id)
            .where(GameRegistration.game_id == game.id)
        )
        reg_count = len(reg_result.all())

        schedule_text += (
            f"╔════════════════════════════╗\n"
            f"║ <b>{game.title}</b>\n"
            f"║ 📅 {game.date.strftime('%d.%m.%Y')} ({game.date.strftime('%A')})\n"
            f"║ 🕐 {game.time_start.strftime('%H:%M')}\n"
            f"╠════════════════════════════╣\n"
            f"║ 🎯 {game.game_type.upper()}\n"
            f"║ 📍 {location.name}\n"
            f"║ 👥 Записано: {reg_count}/{game.max_players}\n"
            f"║ 💰 Ціна: {game.price}₴\n"
            f"╚════════════════════════════╝\n\n"
        )

    await callback.message.edit_text(schedule_text)
    await callback.answer()


@router.callback_query(F.data == "schedule_my")
async def show_my_registrations(callback: CallbackQuery, session: AsyncSession):
    """Show user's game registrations."""
    user = await get_user_by_telegram_id(session, callback.from_user.id)

    if not user:
        await callback.answer("❌ Спочатку пройди реєстрацію!", show_alert=True)
        return

    # Get user's registrations for upcoming games
    today = date.today()

    result = await session.execute(
        select(GameRegistration, Game, Location)
        .join(Game, GameRegistration.game_id == Game.id)
        .join(Location, Game.location_id == Location.id)
        .where(
            and_(
                GameRegistration.user_id == user.telegram_id,
                Game.date >= today
            )
        )
        .order_by(Game.date, Game.time_start)
    )

    registrations = result.all()

    if not registrations:
        await callback.message.edit_text(
            "📋 У тебе немає записів на майбутні ігри.\n\n"
            "Переглянь розклад та запишись на гру!"
        )
        return

    my_games_text = "📋 <b>МОЇ МАЙБУТНІ ІГРИ:</b>\n\n"

    for reg, game, location in registrations:
        payment_status_icon = "✅" if reg.payment_status == "paid" else "⏳"

        my_games_text += (
            f"{payment_status_icon} <b>{game.title}</b>\n"
            f"   📅 {game.date.strftime('%d.%m.%Y')} в {game.time_start.strftime('%H:%M')}\n"
            f"   📍 {location.name}\n"
            f"   💰 Оплата: {reg.payment_status}\n\n"
        )

    await callback.message.edit_text(my_games_text)
    await callback.answer()


@router.callback_query(F.data == "schedule_archive")
async def show_games_archive(callback: CallbackQuery, session: AsyncSession):
    """Show completed games archive."""
    # Get completed games
    result = await session.execute(
        select(Game, Location)
        .join(Location, Game.location_id == Location.id)
        .where(Game.status == "completed")
        .order_by(Game.date.desc())
        .limit(5)
    )

    games = result.all()

    if not games:
        await callback.message.edit_text(
            "📜 Архів ігор порожній.\n"
            "Тут з'являться завершені ігри."
        )
        return

    archive_text = "📜 <b>АРХІВ ІГОР:</b>\n\n"

    for game, location in games:
        archive_text += (
            f"• <b>{game.title}</b>\n"
            f"  {game.date.strftime('%d.%m.%Y')} | {location.name}\n\n"
        )

    await callback.message.edit_text(archive_text)
    await callback.answer()
