# Используем легкий официальный образ Python
FROM python:3.12-slim

# Запрещаем Python создавать .pyc файлы и включаем мгновенный вывод логов
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только зависимости, чтобы Docker кэшировал этот слой
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код бэкенда
COPY . .

# Запускаем FastAPI через Uvicorn на порту 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
