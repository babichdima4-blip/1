"""Achievements handlers."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline import get_achievements_keyboard, get_achievement_detail_keyboard
from bot.services.achievement_service import (
    get_user_achievements,
    get_achievement_stats,
    claim_achievement_rewards,
)
from bot.services.user_service import get_user_by_telegram_id

router = Router(name="achievements")


@router.message(Command("achievements"))
@router.message(F.text == "🎖️ Ачівки")
async def cmd_achievements(message: Message, session: AsyncSession):
    """Handle achievements command."""
    user = await get_user_by_telegram_id(session, message.from_user.id)

    if not user:
        await message.answer("❌ Спочатку пройди реєстрацію: /start")
        return

    # Get achievement statistics
    stats = await get_achievement_stats(session, user.telegram_id)

    # Get user's achievements
    user_achievements = await get_user_achievements(session, user.telegram_id)

    # Categorize achievements
    categories = {
        "activity": {"name": "АКТИВНІСТЬ", "icon": "📊", "achievements": []},
        "victories": {"name": "ПЕРЕМОГИ", "icon": "🏆", "achievements": []},
        "mastery": {"name": "МАЙСТЕРНІСТЬ", "icon": "⭐", "achievements": []},
        "team": {"name": "КОМАНДА", "icon": "👥", "achievements": []},
        "hidden": {"name": "ПРИХОВАНІ", "icon": "❓", "achievements": []},
    }

    for user_ach, achievement in user_achievements:
        if achievement.category in categories:
            categories[achievement.category]["achievements"].append(
                (user_ach, achievement)
            )

    # Format message
    achievements_text = (
        f"🎖️ <b>МОЇ ДОСЯГНЕННЯ</b>\n\n"
        f"Прогрес: {stats['completed']}/{stats['total']} ({stats['percentage']}%)\n\n"
    )

    for cat_code, cat_data in categories.items():
        cat_achievements = cat_data["achievements"]
        if not cat_achievements and cat_code == "hidden":
            continue  # Skip hidden category if no achievements

        completed_in_cat = sum(1 for ua, _ in cat_achievements if ua.is_completed)
        total_in_cat = len(cat_achievements)

        achievements_text += (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{cat_data['icon']} <b>{cat_data['name']}</b> "
            f"({completed_in_cat}/{total_in_cat})\n\n"
        )

        if cat_achievements:
            for user_ach, achievement in cat_achievements[:3]:  # Show first 3
                if achievement.is_hidden and not user_ach.is_completed:
                    achievements_text += "🔒 <i>???</i>\n   Приховане досягнення\n\n"
                else:
                    status_icon = "✅" if user_ach.is_completed else "🔄"
                    claimed_icon = " 🎁" if user_ach.is_completed and not user_ach.claimed else ""

                    achievements_text += (
                        f"{status_icon} <b>{achievement.name}</b>{claimed_icon}\n"
                        f"   {achievement.description}\n"
                    )

                    if not user_ach.is_completed and user_ach.progress > 0:
                        achievements_text += f"   Прогрес: {user_ach.progress}\n"

                    achievements_text += "\n"

            if total_in_cat > 3:
                achievements_text += f"   <i>+{total_in_cat - 3} ще...</i>\n\n"

    await message.answer(achievements_text, reply_markup=get_achievements_keyboard())


@router.callback_query(F.data == "achievements_all")
async def show_all_achievements(callback: CallbackQuery, session: AsyncSession):
    """Show all achievements."""
    user = await get_user_by_telegram_id(session, callback.from_user.id)

    if not user:
        await callback.answer("❌ Помилка!", show_alert=True)
        return

    # Get all user achievements
    user_achievements = await get_user_achievements(session, user.telegram_id)

    achievements_text = "🎖️ <b>ВСІ ДОСЯГНЕННЯ</b>\n\n"

    for user_ach, achievement in user_achievements:
        if achievement.is_hidden and not user_ach.is_completed:
            continue

        status_icon = "✅" if user_ach.is_completed else "⏳"
        claimed_icon = " 🎁" if user_ach.is_completed and not user_ach.claimed else ""

        achievements_text += (
            f"{status_icon} <b>{achievement.name}</b>{claimed_icon}\n"
            f"   {achievement.description}\n"
            f"   Нагорода: +{achievement.reward_points} очок\n\n"
        )

    await callback.message.edit_text(
        achievements_text,
        reply_markup=get_achievements_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "achievements_completed")
async def show_completed_achievements(callback: CallbackQuery, session: AsyncSession):
    """Show only completed achievements."""
    user = await get_user_by_telegram_id(session, callback.from_user.id)

    if not user:
        await callback.answer("❌ Помилка!", show_alert=True)
        return

    # Get completed achievements
    user_achievements = await get_user_achievements(
        session, user.telegram_id, completed_only=True
    )

    if not user_achievements:
        await callback.message.edit_text(
            "🎖️ <b>ЗАВЕРШЕНІ ДОСЯГНЕННЯ</b>\n\n"
            "У тебе поки немає завершених досягнень.\n"
            "Грай та виконуй різні активності, щоб їх отримати!",
            reply_markup=get_achievements_keyboard()
        )
        await callback.answer()
        return

    achievements_text = "🎖️ <b>ЗАВЕРШЕНІ ДОСЯГНЕННЯ</b>\n\n"

    for user_ach, achievement in user_achievements:
        claimed_icon = " 🎁" if not user_ach.claimed else ""
        completed_date = user_ach.completed_at.strftime("%d.%m.%Y") if user_ach.completed_at else "---"

        achievements_text += (
            f"✅ <b>{achievement.name}</b>{claimed_icon}\n"
            f"   {achievement.description}\n"
            f"   Отримано: {completed_date}\n"
            f"   Нагорода: +{achievement.reward_points} очок\n\n"
        )

    await callback.message.edit_text(
        achievements_text,
        reply_markup=get_achievements_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("claim_ach_"))
async def claim_achievement(callback: CallbackQuery, session: AsyncSession):
    """Claim achievement rewards."""
    achievement_id = int(callback.data.split("_")[2])

    success = await claim_achievement_rewards(
        session,
        callback.from_user.id,
        achievement_id
    )

    if success:
        await callback.answer("🎉 Нагороду отримано!", show_alert=True)
        # Refresh achievements view
        await cmd_achievements(callback.message, session)
    else:
        await callback.answer("❌ Помилка при отриманні нагороди!", show_alert=True)
