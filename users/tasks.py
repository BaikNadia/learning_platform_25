from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """
    Фоновая задача: деактивирует пользователей,
    которые не заходили более 30 дней.
    """
    # Определяем дату: 30 дней назад от текущего времени
    cutoff_date = timezone.now() - timedelta(days=30)

    # Находим всех активных пользователей, у которых last_login < cutoff_date
    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=cutoff_date
    )

    count = inactive_users.count()
    if count > 0:
        # Деактивируем
        inactive_users.update(is_active=False)
        print(f"Деактивировано {count} пользователей (не заходили с {cutoff_date.strftime('%Y-%m-%d')})")
    else:
        print("Нет неактивных пользователей для деактивации.")

    return f"Обработано: {count} пользователей"
