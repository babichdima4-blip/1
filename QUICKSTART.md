# 🚀 Швидкий старт - Інструкція для чайників

Ця інструкція допоможе тобі запустити Telegram-бота **з нуля**, навіть якщо ти раніше не працював з подібними проектами.

---

## 📋 Зміст

1. [Що потрібно встановити](#1-що-потрібно-встановити)
2. [Створення Telegram бота](#2-створення-telegram-бота)
3. [Завантаження проекту](#3-завантаження-проекту)
4. [Налаштування проекту](#4-налаштування-проекту)
5. [Запуск бота](#5-запуск-бота)
6. [Ініціалізація ачівок](#6-ініціалізація-ачівок)
7. [Тестування бота](#7-тестування-бота)
8. [Зупинка бота](#8-зупинка-бота)
9. [Вирішення проблем](#9-вирішення-проблем)

---

## 1. Що потрібно встановити

### 🪟 Для Windows:

#### 1.1. Встановлюємо Git
1. Йдемо на https://git-scm.com/download/win
2. Завантажуємо та встановлюємо (всі налаштування залишаємо за замовчуванням)
3. Перевіряємо: відкриваємо Command Prompt (cmd) і вводимо:
   ```bash
   git --version
   ```
   Має показати версію Git

#### 1.2. Встановлюємо Docker Desktop
1. Йдемо на https://www.docker.com/products/docker-desktop/
2. Завантажуємо Docker Desktop for Windows
3. Встановлюємо (може знадобитися перезавантаження)
4. Запускаємо Docker Desktop (іконка з китом)
5. Чекаємо поки Docker запуститься (іконка в треї стане зеленою)

#### 1.3. Встановлюємо Python (опціонально, для локального запуску)
1. Йдемо на https://www.python.org/downloads/
2. Завантажуємо Python 3.11 або новіше
3. **ВАЖЛИВО:** При встановленні обов'язково поставте галочку "Add Python to PATH"!
4. Перевіряємо:
   ```bash
   python --version
   ```

### 🍎 Для macOS:

#### 1.1. Встановлюємо Homebrew (якщо ще немає)
Відкриваємо Terminal та вводимо:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 1.2. Встановлюємо Git
```bash
brew install git
```

#### 1.3. Встановлюємо Docker Desktop
1. Йдемо на https://www.docker.com/products/docker-desktop/
2. Завантажуємо Docker Desktop for Mac
3. Встановлюємо
4. Запускаємо Docker Desktop

#### 1.4. Встановлюємо Python (опціонально)
```bash
brew install python@3.11
```

### 🐧 Для Linux (Ubuntu/Debian):

```bash
# Оновлюємо систему
sudo apt update && sudo apt upgrade -y

# Встановлюємо Git
sudo apt install git -y

# Встановлюємо Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Встановлюємо Docker Compose
sudo apt install docker-compose -y

# Встановлюємо Python (опціонально)
sudo apt install python3.11 python3.11-venv python3-pip -y

# Перезавантажуємо систему (для Docker)
sudo reboot
```

---

## 2. Створення Telegram бота

### 2.1. Відкриваємо Telegram

1. Знаходимо бота **@BotFather** в пошуку Telegram
2. Відкриваємо чат і натискаємо **START**

### 2.2. Створюємо нового бота

1. Відправляємо команду: `/newbot`
2. BotFather попросить ім'я бота. Наприклад: `My Airsoft Bot`
3. Потім попросить username (має закінчуватися на `bot`). Наприклад: `my_airsoft_test_bot`
4. **ВАЖЛИВО:** BotFather надішле тобі **TOKEN** - довгий рядок типу:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz1234567
   ```
5. **ЗБЕРЕЖИ ЦЕЙ TOKEN!** Він нам знадобиться далі.

### 2.3. Отримуємо свій Telegram ID

1. Відкриваємо бота **@userinfobot**
2. Натискаємо START
3. Бот покаже твій ID (число типу `123456789`)
4. **ЗБЕРЕЖИ ЦЕЙ ID!** Це буде ID адміністратора.

---

## 3. Завантаження проекту

### 3.1. Створюємо папку для проекту

**Windows:**
```cmd
# Відкриваємо Command Prompt (cmd)
cd C:\Users\ТвоєІм'я\Desktop
mkdir airsoft-bot
cd airsoft-bot
```

**macOS/Linux:**
```bash
# Відкриваємо Terminal
cd ~/Desktop
mkdir airsoft-bot
cd airsoft-bot
```

### 3.2. Клонуємо репозиторій

```bash
git clone <посилання-на-репозиторій> .
```

**Примітка:** Якщо у тебе репозиторій на GitHub, команда буде виглядати так:
```bash
git clone https://github.com/твій-username/назва-репозиторію.git .
```

### 3.3. Перевіряємо, що файли завантажилися

**Windows:**
```cmd
dir
```

**macOS/Linux:**
```bash
ls -la
```

Ти маєш побачити файли: `main.py`, `docker-compose.yml`, `README.md` і т.д.

---

## 4. Налаштування проекту

### 4.1. Створюємо файл з налаштуваннями

1. Копіюємо приклад конфігурації:

**Windows:**
```cmd
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

### 4.2. Редагуємо .env файл

Відкриваємо файл `.env` у будь-якому текстовому редакторі:
- **Windows:** Блокнот, Notepad++, VS Code
- **macOS:** TextEdit, VS Code
- **Linux:** nano, vim, VS Code

Знаходимо та змінюємо наступні рядки:

```env
# Вставляємо TOKEN від BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz1234567

# Вставляємо свій Telegram ID (можна декілька через кому)
ADMIN_IDS=123456789

# Налаштування бази даних (можна залишити як є)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airsoft_bot
DB_USER=postgres
DB_PASSWORD=mysecretpassword123

# Redis (можна залишити як є)
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Адмін-панель (змінити пароль!)
ADMIN_SECRET_KEY=my-super-secret-key-change-me
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Режим розробки
DEBUG=True
LOG_LEVEL=INFO
```

**ВАЖЛИВО:**
- `BOT_TOKEN` - вставити токен від BotFather
- `ADMIN_IDS` - вставити свій Telegram ID
- `DB_PASSWORD` - змінити на надійний пароль
- `ADMIN_PASSWORD` - змінити на надійний пароль

### 4.3. Зберігаємо файл

Збережи `.env` файл і закрий редактор.

---

## 5. Запуск бота

### 5.1. Переконуємося, що Docker запущений

**Windows/macOS:**
- Перевір, що іконка Docker Desktop в треї зелена
- Якщо ні - запусти Docker Desktop і почекай

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl status docker
```

### 5.2. Запускаємо бота через Docker

Відкриваємо термінал/cmd в папці проекту і вводимо:

```bash
docker-compose up -d
```

**Що відбувається:**
- `-d` означає запуск у фоновому режимі
- Docker завантажить всі необхідні компоненти (може зайняти 5-10 хвилин при першому запуску)
- Створить 3 контейнери: база даних (PostgreSQL), кеш (Redis), і сам бот

### 5.3. Переглядаємо логи

Щоб побачити, що відбувається з ботом:

```bash
docker-compose logs -f bot
```

Натисни `Ctrl+C` щоб вийти з перегляду логів (бот продовжить працювати).

### 5.4. Перевіряємо, що все запустилося

```bash
docker-compose ps
```

Ти маєш побачити 3 контейнери зі статусом "Up":
- airsoft_bot
- airsoft_db
- airsoft_redis

---

## 6. Ініціалізація ачівок

Після першого запуску потрібно додати ачівки в базу даних.

### 6.1. Заходимо в контейнер бота

```bash
docker-compose exec bot bash
```

Ти побачиш командний рядок всередині контейнера:
```
root@xxxxx:/app#
```

### 6.2. Запускаємо скрипт ініціалізації

```bash
python scripts/init_achievements.py
```

Ти маєш побачити:
```
🎖️  Initializing achievements...

+ Created achievement: Перші кроки (first_game)
+ Created achievement: Активний гравець (games_5)
...

✅ Successfully initialized 10 achievements!
```

### 6.3. Виходимо з контейнера

```bash
exit
```

---

## 7. Тестування бота

### 7.1. Відкриваємо Telegram

1. Знаходимо свого бота по username (який ти створив у BotFather)
2. Натискаємо **START**

### 7.2. Проходимо реєстрацію

Бот запитає:
1. **Ім'я та прізвище** - введи своє ім'я
2. **Позивний** - придумай nickname
3. **Номер телефону** - введи або /skip
4. **Досвід у страйкболі** - обери варіант

### 7.3. Тестуємо функції

Після реєстрації з'явиться головне меню з кнопками:

- 👤 **Мій профіль** - переглянути свій профіль
- 🏆 **Рейтинг** - подивитися рейтинг (поки порожній)
- 📅 **Розклад** - переглянути ігри (поки порожньо)
- 🎖️ **Ачівки** - переглянути досягнення

Спробуй натиснути **🎖️ Ачівки** - ти маєш побачити список з 10 ачівок!

### 7.4. Команди бота

Спробуй ввести команди вручну:
- `/start` - головне меню
- `/profile` - профіль
- `/rating` - рейтинг
- `/achievements` - ачівки
- `/help` - допомога

---

## 8. Зупинка бота

### 8.1. Зупинити бота (з збереженням даних)

```bash
docker-compose stop
```

Бот зупиниться, але всі дані збережуться.

### 8.2. Запустити знову

```bash
docker-compose start
```

### 8.3. Повністю видалити (включно з даними)

**УВАГА:** Це видалить ВСІ дані з бази!

```bash
docker-compose down -v
```

---

## 9. Вирішення проблем

### ❌ Проблема: "Cannot connect to Docker daemon"

**Рішення:**
- **Windows/macOS:** Запусти Docker Desktop
- **Linux:** `sudo systemctl start docker`

### ❌ Проблема: "Port 5432 already in use"

**Рішення:**
У тебе вже запущений PostgreSQL локально. Два варіанти:

1. **Зупинити локальний PostgreSQL:**
   - Windows: Йди в Сервіси (services.msc), знайди PostgreSQL, зупини
   - macOS: `brew services stop postgresql`
   - Linux: `sudo systemctl stop postgresql`

2. **Змінити порт в docker-compose.yml:**
   Відкрий `docker-compose.yml`, знайди рядок:
   ```yaml
   ports:
     - "5432:5432"
   ```
   Зміни на:
   ```yaml
   ports:
     - "5433:5432"
   ```

### ❌ Проблема: Бот не відповідає

**Рішення:**

1. Перевір логи:
   ```bash
   docker-compose logs bot
   ```

2. Перевір, що BOT_TOKEN правильний у .env файлі

3. Перезапусти бота:
   ```bash
   docker-compose restart bot
   ```

### ❌ Проблема: "Module not found"

**Рішення:**

Перебудуй контейнери:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### ❌ Проблема: База даних не підключається

**Рішення:**

1. Перевір, що PostgreSQL контейнер запущений:
   ```bash
   docker-compose ps
   ```

2. Перезапусти базу даних:
   ```bash
   docker-compose restart postgres
   ```

3. Переглянь логи бази:
   ```bash
   docker-compose logs postgres
   ```

---

## 📊 Корисні команди

### Переглянути логи всіх сервісів
```bash
docker-compose logs -f
```

### Переглянути логи тільки бота
```bash
docker-compose logs -f bot
```

### Зайти в базу даних
```bash
docker-compose exec postgres psql -U postgres -d airsoft_bot
```

Вийти з psql: `\q`

### Перезапустити тільки бота (без БД)
```bash
docker-compose restart bot
```

### Очистити всі Docker дані (радикальне рішення)
```bash
docker system prune -a --volumes
```
**УВАГА:** Це видалить ВСЕ з Docker, не тільки цей проект!

---

## 🎉 Готово!

Якщо ти дійшов до цього моменту - вітаю! Твій бот працює! 🚀

### Що далі?

1. **Тестуй функції** - спробуй всі кнопки та команди
2. **Додай тестові дані** - створи кілька користувачів, щоб перевірити рейтинг
3. **Налаштуй під себе** - зміни тексти, додай нові функції
4. **Розгорни на сервері** - коли все працює локально, можна виставити на VPS

### Потрібна допомога?

- Перегляни логи: `docker-compose logs -f bot`
- Відкрий issue на GitHub
- Напиши в телеграм адміністратору

---

**Happy coding!** 💪

