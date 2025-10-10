from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorOrReadOnly
from .services import create_checkout_session as create_stripe_session
from .tasks import send_course_update_notification


class CourseViewSet(viewsets.ModelViewSet):
    """
    Полный CRUD для курсов.
    - Модераторы: могут просматривать и редактировать все курсы, но НЕ создавать/удалять
    - Обычные пользователи: только свои курсы
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Course.objects.none()
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Запрещаем модераторам создавать курсы"""
        if request.user.groups.filter(name='moderators').exists():
            return Response(
                {"detail": "Модераторы не могут создавать курсы."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Запрещаем модераторам удалять курсы"""

        if request.user.groups.filter(name='moderators').exists():
            return Response(
                {"detail": "Модераторы не могут удалять курсы."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """При полном обновлении — отправляем уведомление подписчикам"""
        response = super().update(request, *args, **kwargs)

        # Только если обновление прошло успешно (200 OK)
        if response.status_code == 200:
            course_id = kwargs['pk']
            # Отправляем задачу в Celery
            send_course_update_notification.delay(course_id)
        return response

    def partial_update(self, request, *args, **kwargs):
        """При частичном обновлении — тоже отправляем уведомление"""
        response = super().partial_update(request, *args, **kwargs)

        if response.status_code == 200:
            course_id = kwargs['pk']
            send_course_update_notification.delay(course_id)
        return response


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список уроков и создание нового"""
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Запрещаем модераторам создавать уроки"""
        if request.user.groups.filter(name='moderators').exists():
            return Response(
                {"detail": "Модераторы не могут создавать уроки."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Lesson.objects.none()
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def destroy(self, request, *args, **kwargs):
        """Запрещаем модераторам удалять уроки"""
        if request.user.groups.filter(name='moderators').exists():
            return Response(
                {"detail": "Модераторы не могут удалять уроки."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class SubscriptionToggleAPIView(APIView):
    """
    Эндпоинт для переключения подписки на курс.
    POST /api/courses/toggle-subscribe/
    Тело: {"course_id": 1}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать 'course_id'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
            is_subscribed = False
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
            is_subscribed = True

        return Response({
            "message": message,
            "is_subscribed": is_subscribed
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """
    Эндпоинт: создаёт сессию оплаты через Stripe.
    Вызывает сервисный слой.
    """
    course_id = request.data.get('course_id')
    if not course_id:
        return Response(
            {"error": "Необходимо указать course_id"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return Response(
            {"error": "Курс не найден"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        result = create_stripe_session(course, request.user.email)
        return Response(result, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
