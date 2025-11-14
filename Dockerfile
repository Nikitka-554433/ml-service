FROM python:3.10-slim

# Системные пакеты (минимально необходимые)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt 
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt || true

# копируем весь проект
COPY . /app

# правильный запуск
CMD ["python", "models/ml_model.py"]

