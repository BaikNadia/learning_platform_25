from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Урок.
    Используется как вложенный в CourseSerializer.
    """

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'video_url',
        ]
        # Поле 'course' исключено, чтобы не дублировать информацию вложенностью


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курс.
    Включает:
    - lesson_count — количество уроков
    - lessons — список всех уроков курса
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'lesson_count',
            'lessons',
        ]

    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков в курсе.
        """
        return obj.lessons.count()
