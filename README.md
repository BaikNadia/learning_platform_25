# 🚀 Learning Platform 25

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2%2B-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST](https://img.shields.io/badge/Django%20REST%20Framework-3.14%2B-red?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24%2B-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey?logo=creativecommons&logoColor=white)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub Stars](https://img.shields.io/github/stars/BaikNadia/learning-platform-25?style=social)](https://github.com/BaikNadia/learning-platform-25)

**Современная учебная платформа для изучения программирования**  
Проект реализован на **Django** и **Django REST Framework (DRF)** с поддержкой управления курсами, уроками и профилями пользователей через REST API.

---

**👩‍💻 Автор:** [BaikNadia](https://github.com/BaikNadia)  
**📦 Репозиторий:** [Learning Platform 25](https://github.com/BaikNadia/learning-platform-25)  
**📜 Лицензия:** [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

---

## 📌 Основные возможности

# Learning Platform 25

Учебная платформа для изучения программирования. Проект реализован на **Django** и **Django REST Framework (DRF)**. Поддерживает управление курсами, уроками, платежами и подписками через REST API.

---

## 📌 Основные возможности

- **JWT-авторизация**: регистрация, вход, обновление токена
- **CRUD для курсов и уроков** через API
- **Модераторы**: могут редактировать все курсы, но не создавать/удалять
- **Подписка на курсы**: переключение одним запросом
- **Владелец объекта**: пользователи видят и редактируют только свои курсы и уроки
- **Оплата курсов через Stripe**:
  - Создание продукта, цены и Checkout Session
  - Поддержка тестовых карт
- **Асинхронная рассылка писем**:
  - При обновлении курса — подписчикам приходит email
  - Реализовано через **Celery**
- **Автоматическая деактивация пользователей**:
  - Через **celery-beat** проверяется `last_login`
  - Пользователи, не заходившие более месяца, блокируются (`is_active = False`)
- **Фильтрация платежей** по курсу, способу оплаты и дате
- **Валидация видео**: разрешены только ссылки на `youtube.com`
- **Тестирование**: полное покрытие ключевых эндпоинтов

---

## 🛠️ Технологии

- Python 3.11
- Django 5.2
- Django REST Framework (DRF)
- JWT (djangorestframework-simplejwt)
- Stripe API
- Redis + Celery + Celery Beat
- PostgreSQL
- Docker + Docker Compose
- Git + GitHub
- Postman (рекомендуется для тестирования API)

---

## Структура проекта
learning_platform_25/
├── config/               # Настройки Django (urls.py, settings.py)
├── materials/            # Модели: Course, Lesson + API
├── users/                # Кастомный User + API профиля
├── media/                # Загружаемые файлы 
├── manage.py
└── requirements.txt      # зависимости

## 🚀 Запуск проекта (локально)

###  Клонируй репозиторий
bash
git clone git@github.com:BaikNadia/learning_platform_25.git
cd learning_platform_25

### Создай и активируй виртуальное окружение
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

### Установи зависимости
pip install django djangorestframework djangorestframework-simplejwt django-filter stripe redis celery django-celery-beat django-redis

### Выполни миграции
python manage.py makemigrations
python manage.py migrate

### Создай суперпользователя
python manage.py createsuperuser

### Загрузи тестовые данные (фикстуры)
python manage.py loaddata payment_data.json

### Запусти сервер
python manage.py runserver

### Запусти Celery Worker:
celery -A config worker -l info -P solo

### Запусти Celery Beat:
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

## 🐳 Запуск через Docker:
1. Убедись, что есть файлы:
.env; docker-compose.yaml; Dockerfile; requirements.txt

2. Собери и запусти:
docker-compose up -d --build

3. Выполни миграции и создай суперпользователя:
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser


# API Эндпоинты
## Авторизация и пользователи
POST /api/token/ — Получить JWT access и refresh токены
POST /api/token/refresh/ — Обновить access токен
POST /api/users/register/ — Регистрация нового пользователя
GET /api/users/me/ — Получить профиль текущего пользователя
PATCH /api/users/me/ — Обновить свой профиль (email, аватар и др.)

## Курсы: /api/courses/
GET /api/courses/ — Список курсов (с lesson_count, is_subscribed, уроками)
POST /api/courses/ — Создать новый курс (не модератор)
GET /api/courses/{id}/ — Просмотр деталей курса
PUT /api/courses/{id}/ — Полное обновление курса (владелец или модератор)
PATCH /api/courses/{id}/ — Частичное обновление курса (владелец или модератор)
DELETE /api/courses/{id}/ — Удалить курс (не модератор)

## Уроки: /api/lessons/
GET /api/lessons/ — Список всех уроков
POST /api/lessons/ — Создать новый урок (обязательно: course, video_url — только YouTube)
GET /api/lessons/{id}/ — Просмотр урока
PUT /api/lessons/{id}/ — Полное обновление урока (владелец)
PATCH /api/lessons/{id}/ — Частичное обновление урока (владелец)
DELETE /api/lessons/{id}/ — Удалить урок (владелец)

## Подписка на курсы
POST /api/courses/toggle-subscribe/
Тело: { "course_id": 1 }
→ Переключает подписку пользователя на курс

## Фильтры:
?paid_course=1 — по курсу
?paid_lesson=1 — по уроку
?payment_method=TRANSFER — по способу (CASH, TRANSFER)
?ordering=payment_date — сортировка по дате (по убыванию: -payment_date)

## Оплата через Stripe
POST /api/lessons/create-checkout-session/
Тело: { "course_id": 1 }
→ Создаёт:
Product (товар в Stripe)
Price (цена)
Checkout Session
→ Возвращает: { "checkout_url": "https://checkout.stripe.com/..." }

## Платежи (просмотр)
GET /api/users/payments/ — Список всех платежей текущего пользователя
GET /api/users/payments/?paid_course=1 — Фильтр по курсу
GET /api/users/payments/?payment_method=card — Фильтр по способу оплаты
GET /api/users/payments/?ordering=-payment_date — Сортировка по дате (новые сначала)

Все эндпоинты требуют авторизации через:
Authorization: Bearer <ваш_jwt_токен>

## Фоновые задачи (Celery & Celery Beat)
materials.tasks.send_course_update_notification(course_id):
По расписанию администратора,
Отправляет email всем подписчикам при обновлении курса.

users.tasks.deactivate_inactive_users():
Ежедневно в 02:00,
Деактивирует пользователей, не заходивших более 30 дней.

