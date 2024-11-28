FROM python:3.11.9-slim

WORKDIR /app

# Копируем requirements.txt в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint.sh в контейнер
COPY entrypoint.sh /entrypoint.sh

# Делаем скрипт исполнимым
RUN chmod +x /entrypoint.sh

COPY . .

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "atomeco.wsgi:application"]