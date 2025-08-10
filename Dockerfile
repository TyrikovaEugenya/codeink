# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Экспонируем порт (Django по умолчанию на 8000)
EXPOSE 8000

# Команда для запуска
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]