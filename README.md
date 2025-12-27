# Airsoft Pro League Bot

Telegram-бот для управління страйкбольним клубом з системою рейтингів, досягнень та винагород.

---

## 🚀 Швидкий старт

### Запуск локально (для тестування):
📖 Дивись **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - швидка інструкція за 5 хвилин

### Запуск на сервері (24/7):
📖 Дивись **[DEPLOY_VPS.md](DEPLOY_VPS.md)** - повна інструкція для VPS

### Детальна інструкція для новачків:
📖 Дивись **[QUICKSTART.md](QUICKSTART.md)** - покрокове пояснення всього

### Вибір хостингу:
📖 Дивись **[HOSTING_COMPARISON.md](HOSTING_COMPARISON.md)** - порівняння всіх варіантів

---

## Функціонал MVP

### ✅ Реалізовано

- [x] **Реєстрація користувачів** - покроковий процес з вибором досвіду
- [x] **Профіль гравця** - система рангів (5 рівнів: Новачок → Легенда)
- [x] **Рейтингова система** - сезонні рейтинги з детальною статистикою
- [x] **Розклад ігор** - перегляд майбутніх ігор та запис
- [x] **Система досягнень** - 10 базових ачівок з винагородами
- [x] **База даних** - PostgreSQL з повною схемою (13 моделей)
- [x] **Docker** - повна контейнеризація для легкого деплою
- [x] **Документація** - 4 детальні гайди для різних сценаріїв

### 🚧 Наступні етапи (Post-MVP)

- [ ] Команди та командний рейтинг
- [ ] Нотифікації та нагадування про ігри
- [ ] Магазин винагород (промокоди, мерч)
- [ ] Адмін-панель (Flask) для управління
- [ ] Сезонні абонементи
- [ ] Розширена система ачівок (85 штук)

## Технології

- **Мова:** Python 3.11+
- **Bot Framework:** aiogram 3.4
- **База даних:** PostgreSQL 15
- **ORM:** SQLAlchemy 2.0 (async)
- **Міграції:** Alembic
- **Кеш/FSM:** Redis 7
- **Адмін-панель:** Flask (в розробці)
- **Контейнеризація:** Docker + Docker Compose

## Структура проекту

```
.
├── bot/                      # Основний код бота
│   ├── handlers/             # Обробники команд
│   │   ├── start.py          # Реєстрація та /start
│   │   ├── profile.py        # Профіль користувача
│   │   ├── rating.py         # Рейтинги
│   │   └── schedule.py       # Розклад ігор
│   ├── keyboards/            # Клавіатури
│   │   ├── main.py           # Головна клавіатура
│   │   └── inline.py         # Inline кнопки
│   ├── middlewares/          # Middleware
│   │   └── db.py             # Сесія БД
│   ├── models/               # Моделі бази даних
│   │   ├── user.py           # Користувачі
│   │   ├── season.py         # Сезони та рейтинг
│   │   ├── team.py           # Команди
│   │   ├── game.py           # Ігри
│   │   ├── achievement.py    # Досягнення
│   │   └── ...
│   ├── services/             # Бізнес-логіка
│   │   └── user_service.py   # Сервіс користувачів
│   └── database.py           # Підключення до БД
├── admin/                    # Адмін-панель (Flask)
├── config/                   # Конфігурація
│   └── settings.py           # Налаштування
├── migrations/               # Міграції Alembic
├── logs/                     # Логи
├── main.py                   # Точка входу
├── docker-compose.yml        # Docker Compose
├── Dockerfile                # Docker образ
├── requirements.txt          # Залежності
└── README.md                 # Документація

```

## Встановлення та запуск

### 1. Клонування репозиторію

```bash
git clone <repository-url>
cd telegram-airsoft-bot
```

### 2. Налаштування змінних оточення

Скопіюйте `.env.example` в `.env` та заповніть необхідні значення:

```bash
cp .env.example .env
```

Відредагуйте `.env`:

```env
# Telegram Bot
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_IDS=123456789

# Database
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airsoft_bot
DB_USER=postgres
DB_PASSWORD=your_strong_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Admin Panel
ADMIN_SECRET_KEY=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin_password
```

### 3. Запуск через Docker Compose (рекомендовано)

```bash
# Запустити всі сервіси
docker-compose up -d

# Переглянути логи
docker-compose logs -f bot

# Зупинити
docker-compose down
```

### 4. Запуск локально (для розробки)

```bash
# Створити віртуальне оточення
python -m venv venv
source venv/bin/activate  # Linux/Mac
# або
venv\Scripts\activate  # Windows

# Встановити залежності
pip install -r requirements.txt

# Запустити PostgreSQL та Redis (через Docker)
docker-compose up -d postgres redis

# Застосувати міграції
alembic upgrade head

# Запустити бота
python main.py
```

## Міграції бази даних

```bash
# Створити нову міграцію
alembic revision --autogenerate -m "Description"

# Застосувати міграції
alembic upgrade head

# Відкотити останню міграцію
alembic downgrade -1

# Переглянути історію
alembic history
```

## Команди бота

### Для користувачів

- `/start` - Початок роботи / Реєстрація
- `/profile` - Мій профіль
- `/rating` - Рейтинг гравців
- `/schedule` - Розклад ігор
- `/help` - Довідка

### Кнопки меню

- 👤 Мій профіль
- 🏆 Рейтинг
- 📅 Розклад
- 👥 Команди
- 🎖️ Ачівки
- 🛒 Магазин
- ❓ Допомога

## Система рангів

| Ранг | Іконка | Очки | Знижка |
|------|--------|------|--------|
| Новачок | 🟢 | 0-200 | 0% |
| Гравець | 🔵 | 201-500 | 5% |
| Досвідчений | 🟣 | 501-1000 | 10% |
| Ветеран | 🟡 | 1001-2000 | 15% |
| Легенда | 🔴 | 2000+ | 20% |

## Нарахування очок

### Базові очки:
- Участь: +10
- Перемога: +5
- Виконання місії: +3
- MVP: +5
- Асист: +2
- Захоплення точки: +2

### Множники:
- **День тижня:**
  - Понеділок-П'ятниця: ×0.7
  - Субота: ×1.0
  - Неділя: ×1.2

- **Тип гри:**
  - Regular: ×1.0
  - Tournament: ×1.5
  - Night: ×1.3
  - CQB: ×1.2
  - Special: ×1.4

## Розробка

### Додавання нового handler

1. Створіть файл в `bot/handlers/`
2. Створіть Router
3. Додайте обробники подій
4. Зареєструйте router в `bot/handlers/__init__.py`

Приклад:

```python
from aiogram import Router
from aiogram.filters import Command

router = Router(name="feature")

@router.message(Command("feature"))
async def cmd_feature(message: Message):
    await message.answer("Feature!")
```

### Додавання нової моделі

1. Створіть файл в `bot/models/`
2. Успадкуйте від `Base`
3. Додайте в `bot/models/__init__.py`
4. Створіть міграцію: `alembic revision --autogenerate -m "Add feature model"`
5. Застосуйте: `alembic upgrade head`

## Тестування

```bash
# Запустити тести (коли будуть додані)
pytest

# З coverage
pytest --cov=bot tests/
```

## Логування

Логи зберігаються в:
- `logs/bot.log` - логи бота
- Консоль (stdout)

Рівні логування налаштовуються в `.env` через `LOG_LEVEL`.

## Troubleshooting

### Бот не запускається

1. Перевірте `.env` файл
2. Перевірте чи запущені PostgreSQL та Redis
3. Перегляньте логи: `docker-compose logs bot`

### Помилки бази даних

1. Перевірте підключення: `docker-compose ps`
2. Застосуйте міграції: `alembic upgrade head`
3. Перезапустіть сервіси: `docker-compose restart`

### Бот не відповідає

1. Перевірте токен бота в `.env`
2. Перевірте чи бот не заблокований Telegram
3. Перегляньте логи на помилки

## Roadmap

### Фаза 1: MVP (поточна)
- [x] Базова реєстрація
- [x] Профілі
- [x] Рейтинг
- [ ] 10 базових ачівок
- [ ] Базова адмін-панель

### Фаза 2: Розширення
- [ ] Повна система ачівок (85 шт)
- [ ] Команди
- [ ] Магазин винагород
- [ ] Абонементи
- [ ] Реферальна програма

### Фаза 3: Розвинена версія
- [ ] Мобільний додаток
- [ ] Інтеграція з e-commerce
- [ ] Live tracking
- [ ] ML прогнози

## Контакти

- **Telegram:** @your_telegram
- **Email:** your@email.com
- **Website:** https://airsoftpro.ua

## Ліцензія

MIT License - див. LICENSE файл

## Автори

- Розробник - Ваше ім'я

---

**Статус проекту:** 🚧 В активній розробці (MVP фаза)
