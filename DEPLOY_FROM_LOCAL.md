# 🚀 Як направити бота з локалки на VPS

Є кілька способів перенести код з твого комп'ютера на VPS.

---

## Спосіб 1: Через Git (НАЙКРАЩИЙ) ⭐

### На локальному комп'ютері:

```bash
# 1. Переконайся що все закомічено
git add -A
git commit -m "Ready for deployment"
git push origin claude/telegram-airsoft-bot-uqVId
```

### На VPS:

```bash
# 1. Підключись до VPS
ssh root@твій-IP

# 2. Клонуй репозиторій
cd ~
git clone https://github.com/твій-username/твій-репо.git airsoft-bot
cd airsoft-bot

# 3. Переключись на потрібну гілку
git checkout claude/telegram-airsoft-bot-uqVId

# 4. Налаштуй .env
cp .env.example .env
nano .env
# Вставляй BOT_TOKEN, ADMIN_IDS і т.д.
# ВАЖЛИВО: DB_HOST=postgres (не localhost!)

# 5. Запусти
docker-compose up -d

# 6. Ініціалізуй ачівки
docker-compose exec bot python scripts/init_achievements.py
```

**Готово!** Бот працює на VPS! 🎉

---

## Спосіб 2: Через SCP (якщо немає GitHub)

### З Windows (PowerShell):

```powershell
# Копіюємо всю папку на VPS
scp -r C:\path\to\airsoft-bot root@твій-IP:/root/

# Підключаємось до VPS
ssh root@твій-IP

# На VPS:
cd ~/airsoft-bot
cp .env.example .env
nano .env  # Налаштуй .env
docker-compose up -d
docker-compose exec bot python scripts/init_achievements.py
```

### З macOS/Linux:

```bash
# Копіюємо всю папку на VPS
scp -r ~/Desktop/airsoft-bot root@твій-IP:/root/

# Підключаємось до VPS
ssh root@твій-IP

# На VPS:
cd ~/airsoft-bot
cp .env.example .env
nano .env  # Налаштуй .env
docker-compose up -d
docker-compose exec bot python scripts/init_achievements.py
```

---

## Спосіб 3: Через rsync (найшвидше для оновлень)

### З macOS/Linux:

```bash
# Перша синхронізація
rsync -avz --exclude 'venv' --exclude '__pycache__' \
  ~/Desktop/airsoft-bot/ root@твій-IP:/root/airsoft-bot/

# Підключаємось до VPS
ssh root@твій-IP
cd ~/airsoft-bot
docker-compose up -d
```

**Для наступних оновлень:**
```bash
# Локально - синхронізуємо зміни
rsync -avz --exclude 'venv' --exclude '__pycache__' \
  ~/Desktop/airsoft-bot/ root@твій-IP:/root/airsoft-bot/

# На VPS - перезапускаємо
ssh root@твій-IP "cd ~/airsoft-bot && docker-compose restart bot"
```

---

## Спосіб 4: Через Docker Hub (для продвинутих)

### 1. На локальному комп'ютері:

```bash
# Логінимось в Docker Hub
docker login

# Будуємо образ
docker build -t твій-username/airsoft-bot:latest .

# Пушимо на Docker Hub
docker push твій-username/airsoft-bot:latest
```

### 2. На VPS:

```bash
# Змінюємо docker-compose.yml
nano docker-compose.yml
```

Замість `build: .` вкажи:
```yaml
bot:
  image: твій-username/airsoft-bot:latest
  # build: .  <- закоментуй цей рядок
```

```bash
# Запускаємо
docker-compose pull
docker-compose up -d
```

---

## ⚙️ Автоматизація оновлень

Створи скрипт на VPS для швидкого оновлення:

```bash
# На VPS створюємо скрипт
nano ~/update-bot.sh
```

Вставляємо:
```bash
#!/bin/bash
cd ~/airsoft-bot
git pull origin claude/telegram-airsoft-bot-uqVId
docker-compose build --no-cache bot
docker-compose restart bot
docker-compose logs -f bot
```

Робимо виконуваним:
```bash
chmod +x ~/update-bot.sh
```

**Тепер для оновлення просто:**
```bash
./update-bot.sh
```

---

## 🔄 Workflow для розробки

### 1. Розробка локально:
```bash
# Локально працюємо та тестуємо
docker-compose up

# Коли все працює - комітимо
git add -A
git commit -m "New feature"
git push origin claude/telegram-airsoft-bot-uqVId
```

### 2. Деплой на VPS:
```bash
# SSH на VPS
ssh root@твій-IP

# Оновлюємо код
cd ~/airsoft-bot
git pull
docker-compose restart bot

# Перевіряємо логи
docker-compose logs -f bot
```

---

## 📝 Чек-лист деплою:

- [ ] Код закомічений і запушений на GitHub
- [ ] VPS створений і Docker встановлений
- [ ] Проект клонований на VPS
- [ ] `.env` файл налаштований (DB_HOST=postgres!)
- [ ] `docker-compose up -d` виконано
- [ ] Ачівки ініціалізовані
- [ ] Бот відповідає в Telegram
- [ ] Логи чисті (немає помилок)
- [ ] Автозапуск налаштований (systemd)

---

## 🆘 Troubleshooting

### Помилка підключення до БД:
→ Дивись [QUICK_FIX_VPS.md](QUICK_FIX_VPS.md)

### Помилка при git clone (приватний репозиторій):
```bash
# Використовуй Personal Access Token
git clone https://твій-токен@github.com/username/repo.git
```

### Забув що змінив у коді:
```bash
git status
git diff
```

### Хочу відкотити зміни на VPS:
```bash
cd ~/airsoft-bot
git reset --hard HEAD
git pull
docker-compose restart bot
```

---

**Готово! Бот на VPS і працює 24/7! 🚀**
