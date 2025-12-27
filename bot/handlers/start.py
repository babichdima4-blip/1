"""Start and registration handlers."""
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.main import get_main_keyboard
from bot.keyboards.inline import get_registration_keyboard
from bot.models import User
from bot.services.user_service import create_user, get_user_by_telegram_id

router = Router(name="start")


class RegistrationStates(StatesGroup):
    """Registration states."""
    waiting_for_name = State()
    waiting_for_nickname = State()
    waiting_for_phone = State()
    waiting_for_experience = State()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    """Handle /start command."""
    user = await get_user_by_telegram_id(session, message.from_user.id)

    if user:
        # User already registered
        await message.answer(
            f"Вітаю знову, <b>{user.nickname}</b>! 👋\n\n"
            f"Твій ранг: {user.current_rank.capitalize()} 🏆\n"
            f"Історичних очок: {user.total_historical_points}\n\n"
            f"Обери дію з меню нижче:",
            reply_markup=get_main_keyboard()
        )
    else:
        # New user - start registration
        await message.answer(
            "👋 <b>Вітаємо в Airsoft Pro League!</b>\n\n"
            "Це бот страйкбольного клубу з системою рейтингів, "
            "досягнень і винагород.\n\n"
            "Давай почнемо реєстрацію!\n\n"
            "Як тебе звати? (Ім'я та прізвище)"
        )
        await state.set_state(RegistrationStates.waiting_for_name)


@router.message(RegistrationStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    """Process user's name."""
    name_parts = message.text.strip().split(maxsplit=1)

    if len(name_parts) < 2:
        await message.answer(
            "❌ Будь ласка, вкажи ім'я <b>та</b> прізвище.\n"
            "Наприклад: Олексій Петренко"
        )
        return

    first_name, last_name = name_parts
    await state.update_data(first_name=first_name, last_name=last_name)

    await message.answer(
        f"Чудово, {first_name}! 👍\n\n"
        "Тепер вкажи свій <b>позивний</b> (nickname).\n"
        "Він буде відображатися в рейтингах."
    )
    await state.set_state(RegistrationStates.waiting_for_nickname)


@router.message(RegistrationStates.waiting_for_nickname)
async def process_nickname(message: Message, session: AsyncSession, state: FSMContext):
    """Process user's nickname."""
    nickname = message.text.strip()

    if len(nickname) < 3 or len(nickname) > 20:
        await message.answer(
            "❌ Позивний має бути від 3 до 20 символів.\n"
            "Спробуй ще раз:"
        )
        return

    # Check if nickname is already taken
    result = await session.execute(
        select(User).where(User.nickname == nickname)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        await message.answer(
            f"❌ Позивний <b>{nickname}</b> вже зайнятий.\n"
            "Спробуй інший:"
        )
        return

    await state.update_data(nickname=nickname)

    await message.answer(
        "Відмінно! 💪\n\n"
        "Тепер поділися своїм <b>номером телефону</b>.\n"
        "Це потрібно для зв'язку щодо ігор.\n\n"
        "Відправ номер у форматі: +380XXXXXXXXX\n"
        "Або напиши /skip, щоб пропустити."
    )
    await state.set_state(RegistrationStates.waiting_for_phone)


@router.message(RegistrationStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    """Process user's phone number."""
    phone = None

    if message.text and message.text != "/skip":
        phone = message.text.strip()

        # Basic phone validation
        if not phone.startswith("+") or len(phone) < 12:
            await message.answer(
                "❌ Некоректний формат номера.\n"
                "Використовуй формат: +380XXXXXXXXX\n\n"
                "Або напиши /skip, щоб пропустити."
            )
            return

    await state.update_data(phone=phone)

    await message.answer(
        "Останнє питання! 🎯\n\n"
        "Який у тебе досвід у страйкболі?\n\n"
        "Обери варіант:",
        reply_markup=get_registration_keyboard()
    )
    await state.set_state(RegistrationStates.waiting_for_experience)


@router.callback_query(RegistrationStates.waiting_for_experience, F.data.startswith("exp_"))
async def process_experience(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext
):
    """Process user's experience level."""
    experience = callback.data.split("_")[1]
    data = await state.get_data()

    # Create user
    user = await create_user(
        session=session,
        telegram_id=callback.from_user.id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        nickname=data["nickname"],
        phone=data.get("phone"),
        experience_level=experience
    )

    await callback.message.delete()
    await callback.message.answer(
        f"🎉 <b>Реєстрація завершена!</b>\n\n"
        f"Вітаємо в клубі, <b>{user.nickname}</b>!\n\n"
        f"📊 Твій профіль:\n"
        f"• Ім'я: {user.full_name}\n"
        f"• Позивний: {user.nickname}\n"
        f"• Рівень: {user.experience_level}\n"
        f"• Ранг: {user.current_rank.capitalize()}\n\n"
        f"Тепер ти можеш:\n"
        f"• Переглядати розклад ігор\n"
        f"• Записуватись на ігри\n"
        f"• Відстежувати свій рейтинг\n"
        f"• Отримувати досягнення\n"
        f"• Приєднатися до команди\n\n"
        f"Обери дію з меню:",
        reply_markup=get_main_keyboard()
    )

    await state.clear()
    await callback.answer()


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = (
        "<b>📚 Довідка</b>\n\n"
        "<b>Основні команди:</b>\n"
        "/start - Головне меню\n"
        "/profile - Мій профіль\n"
        "/rating - Рейтинг гравців\n"
        "/schedule - Розклад ігор\n"
        "/help - Ця довідка\n\n"
        "<b>Про бота:</b>\n"
        "Airsoft Pro League - це система управління страйкбольним клубом "
        "з рейтингами, досягненнями та винагородами.\n\n"
        "З питань звертайся до адміністрації:\n"
        "📞 +380 XX XXX XX XX"
    )
    await message.answer(help_text)
