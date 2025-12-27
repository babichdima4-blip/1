# ⚡ ШВИДКЕ ВИПРАВЛЕННЯ на VPS

Якщо ти вже на VPS і бачиш помилку при `init_achievements.py` - ось швидке рішення:

---

## 🔧 Крок 1: Виправ .env файл

```bash
# На VPS виконай:
cd ~/airsoft-bot
nano .env
```

**Знайди і зміни:**
```env
DB_HOST=postgres      # ← Було localhost, зміни на postgres!
REDIS_HOST=redis      # ← Було localhost, зміни на redis!
```

**Збережи:** `Ctrl+O`, Enter, `Ctrl+X`

---

## 🔧 Крок 2: Перезапусти бота

```bash
docker-compose restart bot
```

Почекай 5 секунд...

---

## 🔧 Крок 3: Ініціалізуй ачівки

```bash
docker-compose exec bot python scripts/init_achievements.py
```

**Маєш побачити:**
```
🎖️  Initializing achievements...

+ Created achievement: Перші кроки (first_game)
+ Created achievement: Активний гравець (games_5)
...
✅ Successfully initialized 10 achievements!
```

---

## ✅ Готово!

Тепер перевір бота в Telegram:
- Відкрий свого бота
- Натисни кнопку **🎖️ Ачівки**
- Маєш побачити список з 10 ачівок!

---

## 📋 Якщо все ще помилка:

**Повна перезборка:**
```bash
cd ~/airsoft-bot
docker-compose down
docker-compose up -d
sleep 10
docker-compose exec bot python scripts/init_achievements.py
```

---

**Працює! 🎉**
