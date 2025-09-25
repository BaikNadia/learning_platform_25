from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorOrReadOnly



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsModeratorOrReadOnly]  # ← используем кастомное разрешение

    def get_queryset(self):
        user = self.request.user
        # Модераторы видят всё
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        # Остальные — только свои курсы
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Разные права в зависимости от действия.
        """
        if self.action in ['create', 'destroy']:
            # Модераторы НЕ могут создавать и удалять
            return [permissions.IsAuthenticated(), ~permissions.IsInGroup('moderators')]
        return [IsModeratorOrReadOnly()]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список уроков и создание нового"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)
    