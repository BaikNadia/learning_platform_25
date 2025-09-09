# Learning Platform 25

Учебная платформа для изучения программирования. Проект реализован на **Django** и **Django REST Framework (DRF)**. Поддерживает управление курсами, уроками и профилями пользователей через REST API.

---

## 📌 Основные возможности

- **Кастомная модель пользователя** с авторизацией по email
- **CRUD для курсов** — реализован через `ViewSet`
- **CRUD для уроков** — реализован через `Generic`-классы
- Редактирование профиля пользователя (`/api/users/me/`)
- Загрузка превью (курсы и уроки) и аватаров
- Полностью работающее REST API, протестированное в Postman

---

## 🛠️ Технологии

- Python 3.x
- Django 5.2
- Django REST Framework (DRF)
- Postgres
- Git + GitHub
- PyCharm (рекомендуемая IDE)

---

## Структура проекта
learning_platform_25/
├── config/               # Настройки Django (urls.py, settings.py)
├── materials/            # Модели: Course, Lesson + API
├── users/                # Кастомный User + API профиля
├── media/                # Загружаемые файлы 
├── manage.py
└── requirements.txt      # зависимости

## Создай и активируй виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

## Установи зависимости
pip install django djangorestframework django-filter

## Выполни миграции
python manage.py makemigrations
python manage.py migrate

## Создай суперпользователя
python manage.py createsuperuser

## Загрузи тестовые данные (фикстуры)
python manage.py loaddata payment_data.json

## Запусти сервер
python manage.py runserver

# API Эндпоинты
## Курсы: /api/courses/
GET — список курсов (с количеством и списком уроков)
POST — создать курс
## Уроки: /api/lessons/
GET — список уроков
POST — создать урок (обязательно: course)
GET /api/lessons/1/ — получить урок
PUT/PATCH — обновить
DELETE — удалить
## Платежи: /api/users/payments/
GET — список платежей
## Фильтры:
?paid_course=1 — по курсу
?paid_lesson=1 — по уроку
?payment_method=TRANSFER — по способу (CASH, TRANSFER)
?ordering=payment_date — сортировка по дате (по убыванию: -payment_date)
## Профиль: /api/users/me/
GET — получить профиль
PATCH — обновить (имя, телефон, город, аватар)
