FROM python:3.11

WORKDIR /app

# Копировать .env файл
COPY .env .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]