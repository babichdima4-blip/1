# 🚨 ВИПРАВЛЕННЯ: Container is restarting

Якщо бачиш помилку `Container is restarting, wait until the container is running` - бот падає при запуску.

---

## 🔍 Крок 1: Дивимося логи

```bash
# Подивись що не так
docker-compose logs bot

# Або останні 50 рядків
docker-compose logs --tail=50 bot
```

**Шукай червоні помилки (ERROR, CRITICAL, Exception)**

---

## 🔧 Найчастіші причини:

### Причина 1: Неправильний DB_HOST (НАЙЧАСТІШЕ!)

**Симптом в логах:**
```
asyncpg.exceptions.CannotConnectNowError
Connect call failed ('127.0.0.1', 5432)
```

**Рішення:**
```bash
nano .env

# Зміни:
DB_HOST=postgres     # НЕ localhost!
REDIS_HOST=redis     # НЕ localhost!

# Збережи: Ctrl+O, Enter, Ctrl+X

# Перезапусти
docker-compose down
docker-compose up -d
```

---

### Причина 2: Неправильний BOT_TOKEN

**Симптом в логах:**
```
Unauthorized
Invalid token
```

**Рішення:**
```bash
nano .env

# Перевір що BOT_TOKEN правильний (від BotFather)
BOT_TOKEN=123456789:ABCdefGHI...

# Збережи та перезапусти
docker-compose restart bot
```

---

### Причина 3: База даних не готова

**Симптом в логах:**
```
Connection refused
could not connect to server
```

**Рішення:**
```bash
# Перевір чи працює PostgreSQL
docker-compose ps

# Якщо postgres не "Up" - запусти
docker-compose up -d postgres

# Почекай 10 секунд
sleep 10

# Перезапусти бота
docker-compose restart bot
```

---

### Причина 4: Помилка в коді

**Симптом в логах:**
```
ImportError
ModuleNotFoundError
SyntaxError
```

**Рішення:**
```bash
# Перебудуй контейнер
docker-compose down
docker-compose build --no-cache bot
docker-compose up -d
```

---

## ⚡ Швидке повне виправлення

Якщо не знаєш що не так - зроби це:

```bash
cd ~/airsoft-bot

# 1. Зупини все
docker-compose down

# 2. Перевір .env файл
cat .env | grep DB_HOST
# Має показати: DB_HOST=postgres (НЕ localhost!)

# Якщо показує localhost - виправ:
nano .env
# Зміни DB_HOST=postgres та REDIS_HOST=redis

# 3. Запусти знову
docker-compose up -d

# 4. Дивись логи в реальному часі
docker-compose logs -f bot
```

**Натисни Ctrl+C коли побачиш "Bot started successfully!"**

---

## 📋 Правильна послідовність запуску:

```bash
# 1. Зупинка всього
docker-compose down

# 2. Запуск бази даних
docker-compose up -d postgres redis

# 3. Почекати 10 секунд
sleep 10

# 4. Запуск бота
docker-compose up -d bot

# 5. Перевірка логів
docker-compose logs -f bot
```

---

## 🔍 Детальна діагностика

### Перевірка всіх контейнерів:
```bash
docker-compose ps
```

**Правильний вивід:**
```
     Name                   State
----------------------------------------
airsoft_bot       Up
airsoft_db        Up (healthy)
airsoft_redis     Up
```

**Якщо бот "Restarting"** - дивись логи!

### Перевірка .env:
```bash
cat .env
```

**Має бути:**
```env
BOT_TOKEN=твій_токен_від_botfather
ADMIN_IDS=твій_telegram_id
DB_HOST=postgres          # ← ВАЖЛИВО!
DB_PORT=5432
DB_NAME=airsoft_bot
DB_USER=postgres
DB_PASSWORD=твій_пароль
REDIS_HOST=redis          # ← ВАЖЛИВО!
REDIS_PORT=6379
```

### Тест підключення до бази:
```bash
docker-compose exec postgres pg_isready -U postgres
```

Має показати: `accepting connections`

---

## 🆘 Якщо нічого не допомагає:

### Повна перебудова з нуля:

```bash
# УВАГА: Це видалить ВСІ дані!

# 1. Видаляємо все
docker-compose down -v
docker system prune -f

# 2. Перевіряємо .env
nano .env
# DB_HOST=postgres
# REDIS_HOST=redis

# 3. Будуємо з нуля
docker-compose build --no-cache

# 4. Запускаємо
docker-compose up -d

# 5. Чекаємо 30 секунд
sleep 30

# 6. Дивимось логи
docker-compose logs -f bot

# 7. Якщо все ОК - ініціалізуємо ачівки
docker-compose exec bot python scripts/init_achievements.py
```

---

## ✅ Як зрозуміти що працює:

**В логах бота маєш побачити:**
```
INFO - Starting Airsoft Pro League Bot...
INFO - Database initialized
INFO - Bot started successfully!
```

**Перевірка в Telegram:**
- Відкрий бота
- Натисни /start
- Маєш побачити привітання та кнопки

---

## 📞 Швидка допомога:

**1. Покажи логи:**
```bash
docker-compose logs --tail=100 bot
```
Скопіюй останні 20-30 рядків з помилками

**2. Покажи статус:**
```bash
docker-compose ps
```

**3. Покажи .env (без паролів!):**
```bash
cat .env | grep -E "DB_HOST|REDIS_HOST|BOT_TOKEN"
```

---

**З цими командами ти знайдеш проблему! 🔍**
