#!/bin/sh

echo "🔍 Checking environment..."
echo "➡️  DEBUG=$DEBUG"
echo "➡️  ALLOWED_HOSTS=$ALLOWED_HOSTS"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate --noinput

# Выдаем права администратора
echo "🔐 Granting superuser rights to 'admin'..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    admin_user = User.objects.get(username='admin')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()
    print("✅ Пользователь 'admin' теперь имеет права администратора")
except User.DoesNotExist:
    print("❌ Пользователь 'admin' не найден")
EOF

# Собираем статику (если будет в будущем)
# python manage.py collectstatic --noinput

# Запускаем сервер
echo "Starting Gunicorn server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers 3