FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    postgresql-client \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя приложения
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Настройка прав
RUN chown -R appuser:appuser /app
USER appuser

# Открытие порта
EXPOSE 8000

# Команда по умолчанию
CMD ["gunicorn", "furnace_optimizer.wsgi:application", "--bind", "0.0.0.0:8000"]