#!/bin/sh

echo "🔍 Checking environment..."
echo "➡️  DEBUG=$DEBUG"
echo "➡️  ALLOWED_HOSTS=$ALLOWED_HOSTS"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate --noinput

# Собираем статику (если будет в будущем)
# python manage.py collectstatic --noinput

# Запускаем сервер
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers 3