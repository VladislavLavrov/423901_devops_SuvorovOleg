# Базовый образ
FROM python:3.12-slim

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаём директорию в контейнере
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]