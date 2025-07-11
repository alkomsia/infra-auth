# Используйте базовый образ Python
FROM python:3.11-slim

# Установите зависимости для виртуального окружения
RUN apt-get update && apt-get install -y python3-venv

# Установите рабочую директорию
WORKDIR /app

# Копируйте файл requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Создайте и активируйте виртуальное окружение
RUN python3 -m venv /venv

# Активируйте виртуальное окружение и установите зависимости
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Убедитесь, что виртуальное окружение активировано при запуске
CMD ["/venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



