from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer



class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD для курса: полный доступ через ViewSet
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Список уроков и создание нового"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    