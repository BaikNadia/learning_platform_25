# Learning Platform 25

Учебная платформа для изучения программирования. Проект реализован на **Django** и **Django REST Framework (DRF)**. Поддерживает управление курсами, уроками и профилями пользователей через REST API.

---

## 📌 Основные возможности

# Learning Platform 25

Учебная платформа для изучения программирования. Проект реализован на **Django** и **Django REST Framework (DRF)**. Поддерживает управление курсами, уроками, платежами и подписками через REST API.

---

## 📌 Основные возможности

- **Кастомный пользователь** с авторизацией по email
- **JWT-авторизация**: регистрация, вход, обновление токена
- **CRUD для курсов и уроков** через API
- **Модераторы**: могут редактировать все курсы, но не создавать/удалять
- **Подписка на курсы**: переключение одним запросом
- **Владелец объекта**: пользователи видят и редактируют только свои курсы и уроки
- **Оплата курсов через Stripe**:
  - Создание продукта и цены
  - Генерация ссылки на оплату
  - Поддержка тестовых карт
- **Фильтрация платежей** по курсу, способу оплаты и дате
- **Валидация видео**: разрешены только ссылки на `youtube.com`
- **Тестирование**: полное покрытие ключевых эндпоинтов

---

## 🛠️ Технологии

- Python 3.x
- Django 5.2
- Django REST Framework (DRF)
- JWT (djangorestframework-simplejwt)
- Stripe API
- Postgres
- Git + GitHub
- PyCharm (рекомендуемая IDE)
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
pip install django djangorestframework django-filter

### Выполни миграции
python manage.py makemigrations
python manage.py migrate

### Создай суперпользователя
python manage.py createsuperuser

### Загрузи тестовые данные (фикстуры)
python manage.py loaddata payment_data.json

### Запусти сервер
python manage.py runserver

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

