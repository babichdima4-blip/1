# ⚡ Швидка інструкція для запуску

## 📋 Що тобі потрібно:

1. **Docker Desktop** - завантаж з https://www.docker.com/products/docker-desktop/
2. **Telegram Bot Token** - отримай у @BotFather
3. **Твій Telegram ID** - дізнайся у @userinfobot

---

## 🚀 Запуск за 5 хвилин:

### 1️⃣ Скопіюй приклад налаштувань:
```bash
cp .env.example .env
```

### 2️⃣ Відкрий `.env` файл і вставсвій токен та ID:
```env
BOT_TOKEN=твій_токен_від_botfather
ADMIN_IDS=твій_telegram_id
DB_PASSWORD=придумай_надійний_пароль
```

### 3️⃣ Запусти Docker Desktop (зачекай поки запуститься)

### 4️⃣ Запусти бота:
```bash
docker-compose up -d
```

### 5️⃣ Ініціалізуй ачівки:
```bash
docker-compose exec bot python scripts/init_achievements.py
```

### 6️⃣ Готово! Знайди свого бота в Telegram і натисни START

---

## 🔍 Корисні команди:

**Переглянути логи:**
```bash
docker-compose logs -f bot
```

**Зупинити бота:**
```bash
docker-compose stop
```

**Запустити знову:**
```bash
docker-compose start
```

**Перезапустити:**
```bash
docker-compose restart bot
```

**Повністю видалити (включно з даними):**
```bash
docker-compose down -v
```

---

## ❌ Проблеми?

**Бот не відповідає:**
1. Перевір логи: `docker-compose logs bot`
2. Перевір TOKEN у .env файлі
3. Перезапусти: `docker-compose restart bot`

**Docker не запускається:**
- Windows/Mac: Запусти Docker Desktop
- Linux: `sudo systemctl start docker`

**Port 5432 зайнятий:**
- Зупини локальний PostgreSQL або зміни порт в docker-compose.yml

---

## 📚 Детальна інструкція:

Якщо щось не виходить - дивись **QUICKSTART.md** - там пояснено кожен крок детально для новачків!

---

## 🎉 Вітаю, бот працює!

Тепер можеш:
- ✅ Реєструватись через бота
- 👤 Переглядати профіль
- 🏆 Бачити рейтинг
- 🎖️ Отримувати ачівки
- 📅 Переглядати розклад

**Команди бота:**
- `/start` - головне меню
- `/profile` - мій профіль
- `/rating` - рейтинг
- `/achievements` - ачівки
- `/help` - допомога
