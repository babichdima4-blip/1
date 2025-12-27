# 🌐 Запуск бота на VPS/хостингу - Інструкція для чайників

Ця інструкція допоможе розмістити бота на віддаленому сервері, щоб він працював 24/7.

---

## 📋 Зміст

1. [Вибір хостингу](#1-вибір-хостингу)
2. [Підготовка сервера](#2-підготовка-сервера)
3. [Встановлення необхідного ПЗ](#3-встановлення-необхідного-пз)
4. [Завантаження проекту](#4-завантаження-проекту)
5. [Налаштування та запуск](#5-налаштування-та-запуск)
6. [Налаштування автозапуску](#6-налаштування-автозапуску)
7. [Моніторинг та логи](#7-моніторинг-та-логи)
8. [Оновлення бота](#8-оновлення-бота)
9. [Вирішення проблем](#9-вирішення-проблем)

---

## 1. Вибір хостингу

### 🎯 Рекомендовані варіанти:

#### 🥇 **Hetzner Cloud** (найдешевше, Європа)
- **Ціна:** від €4.15/міс (~175₴)
- **Сервер:** 2vCPU, 2GB RAM, 40GB SSD
- **Сайт:** https://www.hetzner.com/cloud
- **Локація:** Німеччина/Фінляндія
- ✅ Найкраще співвідношення ціна/якість

#### 🥈 **DigitalOcean** (популярний, простий)
- **Ціна:** від $6/міс (~240₴)
- **Сервер:** 1vCPU, 1GB RAM, 25GB SSD
- **Сайт:** https://www.digitalocean.com/
- **Локація:** різні (є Франкфурт, Амстердам)
- ✅ Простий інтерфейс, багато документації

#### 🥉 **Vultr** (хороша альтернатива)
- **Ціна:** від $6/міс (~240₴)
- **Сервер:** 1vCPU, 1GB RAM, 25GB SSD
- **Сайт:** https://www.vultr.com/
- **Локація:** різні

#### 💡 **Для тих, хто економить:**

**Contabo** - від €3.99/міс
- Дешево, але повільніша підтримка
- https://contabo.com/

**Oracle Cloud Free Tier** - БЕЗКОШТОВНО назавжди!
- 2 VM з 1GB RAM кожна (або 1 VM з 2GB)
- https://www.oracle.com/cloud/free/
- ⚠️ Складніша реєстрація

### 📊 Мінімальні вимоги для бота:

- **RAM:** 1GB (рекомендовано 2GB)
- **CPU:** 1 ядро
- **Диск:** 10GB
- **ОС:** Ubuntu 22.04 LTS

---

## 2. Підготовка сервера

### 2.1. Створення VPS (приклад на DigitalOcean)

1. **Реєструємося на DigitalOcean:**
   - Йдемо на https://www.digitalocean.com/
   - Реєструємось (потрібна карта для $5 депозиту)
   - Підтверджуємо email

2. **Створюємо Droplet (віртуальний сервер):**
   - Натискаємо **Create** → **Droplets**
   - Вибираємо образ: **Ubuntu 22.04 LTS**
   - Вибираємо план: **Basic** → **$6/month** (1GB RAM)
   - Вибираємо регіон: **Frankfurt** або **Amsterdam**
   - **Authentication:** вибираємо **Password** (придумуємо складний пароль)
   - Hostname: `airsoft-bot-server`
   - Натискаємо **Create Droplet**

3. **Чекаємо 1-2 хвилини** поки сервер створюється

4. **Отримуємо IP-адресу:**
   - Після створення побачиш IP адресу типу: `157.230.123.45`
   - **ЗБЕРЕЖИ ЦЮ АДРЕСУ!**

### 2.2. Підключення до сервера

#### Для Windows:

**Варіант 1: PowerShell (вбудований)**
```powershell
ssh root@157.230.123.45
# Замість 157.230.123.45 підстав свій IP
```

**Варіант 2: PuTTY (якщо PowerShell не працює)**
1. Завантаж PuTTY: https://www.putty.org/
2. Запусти PuTTY
3. Host Name: `root@157.230.123.45`
4. Port: `22`
5. Натисни **Open**
6. Введи пароль

#### Для macOS/Linux:

```bash
ssh root@157.230.123.45
# Замість 157.230.123.45 підстав свій IP
```

При першому підключенні спитає:
```
Are you sure you want to continue connecting (yes/no)?
```
Напиши: `yes` і натисни Enter

Введи пароль (символи не відображаються - це нормально!)

**✅ Якщо побачив `root@airsoft-bot-server:~#` - ти підключився!**

---

## 3. Встановлення необхідного ПЗ

Після підключення до сервера виконай ці команди по черзі:

### 3.1. Оновлення системи

```bash
# Оновлюємо список пакетів
apt update

# Оновлюємо всі пакети
apt upgrade -y
```

Це займе 2-5 хвилин.

### 3.2. Встановлення Git

```bash
apt install git -y
```

### 3.3. Встановлення Docker

```bash
# Завантажуємо скрипт встановлення Docker
curl -fsSL https://get.docker.com -o get-docker.sh

# Запускаємо встановлення
sh get-docker.sh

# Видаляємо скрипт
rm get-docker.sh
```

### 3.4. Встановлення Docker Compose

```bash
# Встановлюємо Docker Compose
apt install docker-compose -y
```

### 3.5. Перевірка встановлення

```bash
# Перевіряємо Docker
docker --version
# Має показати: Docker version 24.x.x

# Перевіряємо Docker Compose
docker-compose --version
# Має показати: docker-compose version 1.29.x або новіше
```

**✅ Якщо все ОК - йдемо далі!**

---

## 4. Завантаження проекту

### 4.1. Клонування з GitHub

Якщо твій проект на GitHub:

```bash
# Переходимо в домашню директорію
cd ~

# Клонуємо репозиторій
git clone https://github.com/твій-username/назва-репо.git airsoft-bot

# Переходимо в папку проекту
cd airsoft-bot

# Перевіряємо, що файли є
ls -la
```

### 4.2. Якщо GitHub приватний

Якщо репозиторій приватний, потрібен Personal Access Token:

1. Йдемо на GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Вибираємо scope: `repo`
4. Копіюємо згенерований токен

Клонуємо з токеном:
```bash
git clone https://твій-токен@github.com/username/repo.git airsoft-bot
```

### 4.3. Альтернатива: завантаження через SCP

Якщо проект у тебе локально:

**З Windows (PowerShell):**
```powershell
scp -r C:\path\to\airsoft-bot root@157.230.123.45:/root/
```

**З macOS/Linux:**
```bash
scp -r ~/Desktop/airsoft-bot root@157.230.123.45:/root/
```

---

## 5. Налаштування та запуск

### 5.1. Створення .env файлу

```bash
# Переходимо в папку проекту (якщо ще не там)
cd ~/airsoft-bot

# Копіюємо приклад
cp .env.example .env

# Редагуємо файл
nano .env
```

Відкриється текстовий редактор. Зміни наступні рядки:

```env
# Токен від BotFather
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Твій Telegram ID
ADMIN_IDS=123456789

# База даних (змінити пароль!)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=airsoft_bot
DB_USER=postgres
DB_PASSWORD=супер_складний_пароль_123

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Адмін-панель (змінити!)
ADMIN_SECRET_KEY=випадковий-рядок-символів-32-довжини
ADMIN_USERNAME=admin
ADMIN_PASSWORD=надійний_пароль_123

# Продакшн режим
DEBUG=False
LOG_LEVEL=INFO
```

**Зберігаємо файл:**
- Натискаємо `Ctrl+O` (збереження)
- Enter (підтвердження)
- `Ctrl+X` (вихід)

### 5.2. Запуск бота

```bash
# Запускаємо всі сервіси
docker-compose up -d

# Перевіряємо, що запустилося
docker-compose ps
```

Має показати 3 контейнери зі статусом "Up":
```
     Name                   Command               State    Ports
-------------------------------------------------------------------
airsoft_bot      python main.py                   Up
airsoft_db       docker-entrypoint.sh postgres    Up      5432/tcp
airsoft_redis    docker-entrypoint.sh redis ...   Up      6379/tcp
```

### 5.3. Перевірка логів

```bash
# Дивимося логи бота
docker-compose logs -f bot
```

Маєш побачити:
```
Bot started successfully!
```

Натисни `Ctrl+C` щоб вийти з перегляду логів (бот продовжить працювати).

### 5.4. Ініціалізація ачівок

```bash
# Заходимо в контейнер
docker-compose exec bot bash

# Запускаємо скрипт
python scripts/init_achievements.py

# Виходимо
exit
```

**✅ БОТ ПРАЦЮЄ!** Тепер він доступний 24/7!

---

## 6. Налаштування автозапуску

Щоб бот автоматично запускався після перезавантаження сервера:

### 6.1. Створення systemd сервісу

```bash
# Створюємо файл сервісу
nano /etc/systemd/system/airsoft-bot.service
```

Вставляємо:

```ini
[Unit]
Description=Airsoft Pro League Telegram Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/root/airsoft-bot
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Зберігаємо: `Ctrl+O`, Enter, `Ctrl+X`

### 6.2. Активація сервісу

```bash
# Перезавантажуємо systemd
systemctl daemon-reload

# Увімкнення автозапуску
systemctl enable airsoft-bot

# Перевірка статусу
systemctl status airsoft-bot
```

Тепер бот буде запускатися автоматично при старті сервера!

---

## 7. Моніторинг та логи

### 7.1. Перегляд логів

```bash
# Логи бота в реальному часі
docker-compose logs -f bot

# Останні 100 рядків логів
docker-compose logs --tail=100 bot

# Логи всіх сервісів
docker-compose logs -f
```

### 7.2. Перевірка статусу

```bash
# Статус контейнерів
docker-compose ps

# Використання ресурсів
docker stats

# Використання диску
df -h

# Використання RAM
free -h
```

### 7.3. Налаштуванняротації логів

Щоб логи не займали багато місця:

```bash
nano /etc/docker/daemon.json
```

Вставляємо:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Зберігаємо і перезапускаємо Docker:

```bash
systemctl restart docker
docker-compose up -d
```

---

## 8. Оновлення бота

Коли виходить нова версія:

### 8.1. Оновлення коду

```bash
# Переходимо в папку проекту
cd ~/airsoft-bot

# Зупиняємо бота
docker-compose down

# Отримуємо нові зміни з Git
git pull origin main
# Або якщо у тебе інша гілка:
# git pull origin назва-гілки

# Перебудовуємо контейнери
docker-compose build --no-cache

# Запускаємо знову
docker-compose up -d

# Перевіряємо логи
docker-compose logs -f bot
```

### 8.2. Оновлення залежностей

Якщо змінився `requirements.txt`:

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 8.3. Міграції бази даних

Якщо є нові міграції:

```bash
docker-compose exec bot bash
alembic upgrade head
exit
```

---

## 9. Вирішення проблем

### ❌ Бот не запускається

**Перевірка логів:**
```bash
docker-compose logs bot
```

**Перезапуск:**
```bash
docker-compose restart bot
```

**Повна перебудова:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### ❌ Проблеми з пам'яттю

**Перевірка використання:**
```bash
free -h
docker stats
```

**Рішення:** Збільш RAM сервера або оптимізуй код.

### ❌ База даних не підключається

**Перевірка:**
```bash
docker-compose ps
docker-compose logs postgres
```

**Перезапуск бази:**
```bash
docker-compose restart postgres
```

### ❌ Диск заповнений

**Перевірка:**
```bash
df -h
```

**Очищення Docker:**
```bash
# Видаляємо невикористані images
docker system prune -a

# Видаляємо старі логи
journalctl --vacuum-time=7d
```

### ❌ Порти зайняті

Якщо порт 5432 зайнятий:

```bash
# Перевіряємо, що слухає порт
netstat -tulpn | grep 5432

# Змінюємо порт в docker-compose.yml
nano docker-compose.yml
```

Зміни:
```yaml
ports:
  - "5433:5432"  # замість 5432:5432
```

---

## 🔒 Безпека

### 10.1. Базові налаштування

```bash
# Створюємо нового користувача (не root)
adduser botadmin

# Додаємо в групу sudo
usermod -aG sudo botadmin

# Додаємо в групу docker
usermod -aG docker botadmin
```

### 10.2. Налаштування Firewall

```bash
# Встановлюємо UFW
apt install ufw -y

# Дозволяємо SSH
ufw allow 22/tcp

# Дозволяємо HTTP/HTTPS (якщо потрібна адмін-панель)
ufw allow 80/tcp
ufw allow 443/tcp

# Увімкнення firewall
ufw enable

# Перевірка статусу
ufw status
```

### 10.3. Налаштування SSH ключів (рекомендовано)

**На локальному комп'ютері:**

```bash
# Генеруємо ключ (якщо немає)
ssh-keygen -t rsa -b 4096

# Копіюємо на сервер
ssh-copy-id root@157.230.123.45
```

Тепер можна підключатися без пароля!

### 10.4. Вимкнення root логіну по паролю

Після налаштування SSH ключів:

```bash
nano /etc/ssh/sshd_config
```

Знайди та зміни:
```
PermitRootLogin prohibit-password
PasswordAuthentication no
```

Перезапусти SSH:
```bash
systemctl restart sshd
```

---

## 📊 Моніторинг

### 11.1. Простий скрипт моніторингу

Створи скрипт для перевірки здоров'я бота:

```bash
nano ~/check-bot.sh
```

Вставляємо:

```bash
#!/bin/bash

cd ~/airsoft-bot

# Перевіряємо чи працює бот
if ! docker-compose ps | grep -q "Up"; then
    echo "Bot is down! Restarting..."
    docker-compose restart bot

    # Відправляємо повідомлення собі в Telegram (опціонально)
    curl -s -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
        -d chat_id=<ТВІЙ_ID> \
        -d text="⚠️ Бот був перезапущений на сервері!"
fi
```

Робимо виконуваним:
```bash
chmod +x ~/check-bot.sh
```

### 11.2. Автоматична перевірка через cron

```bash
crontab -e
```

Додаємо рядок (перевірка кожні 5 хвилин):
```
*/5 * * * * /root/check-bot.sh
```

---

## 🚀 Додаткові покращення

### 12.1. Резервне копіювання

Скрипт бекапу бази даних:

```bash
nano ~/backup-db.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/root/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Бекап PostgreSQL
docker-compose exec -T postgres pg_dump -U postgres airsoft_bot > \
    $BACKUP_DIR/db_backup_$DATE.sql

# Видаляємо бекапи старші 7 днів
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup created: db_backup_$DATE.sql"
```

Робимо виконуваним:
```bash
chmod +x ~/backup-db.sh
```

Додаємо в cron (щодня о 3:00):
```bash
crontab -e
```

```
0 3 * * * /root/backup-db.sh
```

### 12.2. HTTPS для адмін-панелі (з Nginx)

Якщо хочеш захищений доступ до адмін-панелі:

```bash
# Встановлюємо Nginx
apt install nginx certbot python3-certbot-nginx -y

# Створюємо конфіг
nano /etc/nginx/sites-available/airsoft-admin
```

Вставляємо:
```nginx
server {
    listen 80;
    server_name admin.твій-домен.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Активуємо:
```bash
ln -s /etc/nginx/sites-available/airsoft-admin /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# Отримуємо SSL сертифікат
certbot --nginx -d admin.твій-домен.com
```

---

## 📝 Чек-лист після встановлення

- [ ] Сервер створено та підключено
- [ ] Docker та Docker Compose встановлено
- [ ] Проект завантажено
- [ ] .env файл налаштовано
- [ ] Бот запущено та працює
- [ ] Ачівки ініціалізовано
- [ ] Автозапуск налаштовано
- [ ] Firewall налаштовано
- [ ] SSH ключі налаштовано
- [ ] Резервне копіювання налаштовано
- [ ] Моніторинг працює

---

## 🎉 Готово!

Твій бот тепер працює на VPS 24/7! 🚀

### Корисні посилання:

- **Документація Docker:** https://docs.docker.com/
- **Документація DigitalOcean:** https://docs.digitalocean.com/
- **Документація Ubuntu:** https://ubuntu.com/server/docs

### Підтримка:

Якщо виникли проблеми:
1. Подивись логи: `docker-compose logs -f bot`
2. Перевір статус: `docker-compose ps`
3. Створи issue на GitHub

---

**Happy hosting! 💪**
