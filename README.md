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