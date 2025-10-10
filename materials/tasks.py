from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscription


@shared_task
def send_course_update_notification(course_id):
    """
    Пример задачи: отправляет email при обновлении курса.
    """
    # Здесь можно получить курс и отправить уведомление подписчикам
    subject = f"Курс #{course_id} был обновлён!"
    message = "Зайдите и проверьте новые уроки."
    recipient_list = ['student@example.com']  # В реальности — список подписчиков

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    return f"Уведомление о курсе {course_id} отправлено"

@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная задача: отправляет email всем подписчикам курса.
    Вызывается при обновлении курса.
    """
    try:
        # Найдём всех подписчиков
        subscriptions = Subscription.objects.filter(course__id=course_id)
        recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

        if not recipient_list:
            return f"Нет подписчиков для курса {course_id}"

        from .models import Course
        course = Course.objects.get(id=course_id)

        subject = f"Курс '{course.title}' был обновлён!"
        message = (
            f"Здравствуйте!\n\n"
            f"Курс '{course.title}', на который вы подписаны, был обновлён.\n"
            f"Зайдите и проверьте новые материалы:\n"
            f"http://localhost:8000/courses/{course.id}/"
        )

        # Отправляем письмо (в консоль в режиме разработки)
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        return f"Рассылка для курса {course_id} отправлена {len(recipient_list)} пользователям"

    except Exception as e:
        return f"Ошибка при отправке уведомления: {str(e)}"
