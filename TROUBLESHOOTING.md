# 🚨 ВИПРАВЛЕННЯ ПОМИЛКИ: Connection Refused

Якщо ти бачиш помилку `[Errno 111] Connect call failed` при ініціалізації ачівок - це означає, що скрипт не може підключитися до бази даних.

## ❌ Проблема

В `.env` файлі неправильно вказаний хост бази даних:
```env
DB_HOST=localhost  # ❌ НЕ ПРАЦЮЄ в Docker!
```

## ✅ Рішення

### Варіант 1: Виправити .env файл (РЕКОМЕНДОВАНО)

```bash
# Відкрий .env файл
nano .env
```

Знайди рядок `DB_HOST=` і зміни на:
```env
DB_HOST=postgres  # ✅ Назва сервісу з docker-compose.yml
```

Збережи: `Ctrl+O`, Enter, `Ctrl+X`

**Перезапусти бота:**
```bash
docker-compose restart bot
```

**Тепер ініціалізуй ачівки:**
```bash
docker-compose exec bot python scripts/init_achievements.py
```

---

### Варіант 2: Використати готовий скрипт

Я створив скрипт, який все зробить автоматично:

```bash
# Надай права на виконання
chmod +x scripts/init_db.sh

# Запусти скрипт
./scripts/init_db.sh
```

Скрипт:
- Перевірить чи працює база даних
- Виправить підключення
- Ініціалізує ачівки

---

### Варіант 3: Ручна ініціалізація через PostgreSQL

Якщо нічого не допомагає:

```bash
# Заходимо в PostgreSQL контейнер
docker-compose exec postgres psql -U postgres -d airsoft_bot
```

В psql виконай:
```sql
-- Створення таблиці ачівок (якщо ще не існує)
-- Тут буде SQL код...

-- Вихід
\q
```

Потім запусти міграції:
```bash
docker-compose exec bot alembic upgrade head
```

---

## 🔍 Діагностика

### Перевірка чи працює база даних:

```bash
# Статус контейнерів
docker-compose ps

# Має показати postgres з статусом "Up"
```

### Перевірка підключення:

```bash
# Тест підключення до PostgreSQL
docker-compose exec postgres pg_isready -U postgres

# Має показати: accepting connections
```

### Перегляд логів бази даних:

```bash
docker-compose logs postgres
```

---

## 📝 Правильний .env для Docker:

```env
# ✅ ПРАВИЛЬНІ налаштування для Docker

# Telegram
BOT_TOKEN=твій_токен
ADMIN_IDS=твій_id

# Database (для Docker!)
DB_HOST=postgres        # ← НЕ localhost!
DB_PORT=5432
DB_NAME=airsoft_bot
DB_USER=postgres
DB_PASSWORD=твій_пароль

# Redis (для Docker!)
REDIS_HOST=redis        # ← НЕ localhost!
REDIS_PORT=6379
REDIS_DB=0

# Admin
ADMIN_SECRET_KEY=секретний_ключ
ADMIN_USERNAME=admin
ADMIN_PASSWORD=пароль

# Environment
DEBUG=False
LOG_LEVEL=INFO
```

**ВАЖЛИВО:**
- `DB_HOST=postgres` - назва сервісу з `docker-compose.yml`
- `REDIS_HOST=redis` - назва сервісу з `docker-compose.yml`
- **НЕ** використовуй `localhost` всередині Docker контейнерів!

---

## 🔄 Після виправлення:

1. **Перезапусти всі сервіси:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

2. **Перевір логи бота:**
   ```bash
   docker-compose logs -f bot
   ```

   Має показати: `Bot started successfully!`

3. **Ініціалізуй ачівки:**
   ```bash
   docker-compose exec bot python scripts/init_achievements.py
   ```

   Має показати:
   ```
   ✅ Successfully initialized 10 achievements!
   ```

4. **Тестуй бота:**
   - Відкрий бота в Telegram
   - Натисни `/achievements`
   - Маєш побачити 10 ачівок!

---

## 🆘 Якщо все ще не працює:

**Перевір всі контейнери:**
```bash
docker-compose ps
```

Всі 3 контейнери мають бути "Up":
- airsoft_bot
- airsoft_db (postgres)
- airsoft_redis

**Повна перебудова (якщо зовсім нічого не допомагає):**
```bash
# УВАГА: Це видалить всі дані!
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d

# Чекаємо 30 секунд
sleep 30

# Ініціалізуємо ачівки
docker-compose exec bot python scripts/init_achievements.py
```

---

**Готово! Тепер має працювати! 🎉**
