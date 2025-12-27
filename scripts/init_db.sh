#!/bin/bash

# Скрипт для перевірки та виправлення підключення до бази даних

echo "🔍 Перевірка підключення до бази даних..."

# Перевіряємо чи працює PostgreSQL контейнер
if ! docker-compose ps | grep postgres | grep -q "Up"; then
    echo "❌ PostgreSQL контейнер не запущений!"
    echo "Запускаємо..."
    docker-compose up -d postgres
    sleep 5
fi

echo "✅ PostgreSQL контейнер запущений"

# Перевіряємо підключення
echo "🔌 Тестуємо підключення до бази даних..."
docker-compose exec postgres pg_isready -U postgres

if [ $? -eq 0 ]; then
    echo "✅ База даних доступна!"

    # Ініціалізуємо ачівки
    echo ""
    echo "🎖️  Ініціалізація ачівок..."
    docker-compose exec bot python scripts/init_achievements.py
else
    echo "❌ Не вдається підключитися до бази даних"
    echo "Перевір налаштування в .env файлі:"
    echo "  DB_HOST має бути 'postgres' (не localhost!)"
    exit 1
fi
