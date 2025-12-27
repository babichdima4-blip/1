"""Profile handlers."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import get_profile_keyboard
from bot.services.user_service import get_user_by_telegram_id

router = Router(name="profile")


@router.message(Command("profile"))
@router.message(F.text == "👤 Мій профіль")
async def cmd_profile(message: Message, session: AsyncSession):
    """Handle profile command."""
    user = await get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer("❌ Спочатку пройди реєстрацію: /start")
        return

    # Get rank icon
    rank_icons = {
        "newbie": "🟢",
        "player": "🔵",
        "experienced": "🟣",
        "veteran": "🟡",
        "legend": "🔴"
    }
    rank_icon = rank_icons.get(user.current_rank, "⚪")

    profile_text = (
        f"╔════════════════════════════╗\n"
        f"║   {user.full_name}\n"
        f"║   \"{user.nickname}\"\n"
        f"║   ID: #{user.telegram_id}\n"
        f"╠════════════════════════════╣\n"
        f"║ 🏆 Ранг: {user.current_rank.capitalize()} {rank_icon}\n"
        f"║ 💎 Історичних очок: {user.total_historical_points}\n"
        f"║ 📊 Рівень досвіду: {user.experience_level}\n"
        f"╚════════════════════════════╝\n"
    )

    await message.answer(profile_text, reply_markup=get_profile_keyboard())


@router.callback_query(F.data == "profile_stats")
async def show_profile_stats(callback: CallbackQuery, session: AsyncSession):
    """Show detailed profile statistics."""
    # TODO: Implement when season ratings are ready
    await callback.answer("📊 Детальна статистика буде доступна після першої гри!", show_alert=True)


@router.callback_query(F.data == "profile_achievements")
async def show_profile_achievements(callback: CallbackQuery):
    """Show user achievements."""
    # TODO: Implement achievements view
    await callback.answer("🎖️ Система ачівок буде додана найближчим часом!", show_alert=True)


@router.callback_query(F.data == "profile_settings")
async def show_profile_settings(callback: CallbackQuery):
    """Show profile settings."""
    # TODO: Implement settings
    await callback.answer("⚙️ Налаштування в розробці!", show_alert=True)


@router.callback_query(F.data == "profile_history")
async def show_profile_history(callback: CallbackQuery):
    """Show game history."""
    # TODO: Implement game history
    await callback.answer("📜 Історія ігор буде доступна після першої гри!", show_alert=True)
