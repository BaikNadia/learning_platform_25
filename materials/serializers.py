from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Урок.
    Используется как вложенный в CourseSerializer.
    """


    class Meta:
        model = Lesson
        fields = '__all__'
        # fields = [
        #     'id',
        #     'title',
        #     'description',
        #     'preview',
        #     'video_url',
        # ]
        # # Поле 'course' исключено, чтобы не дублировать информацию вложенностью
        read_only_fields = ('owner',)


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
        read_only_fields = ('owner',)

    def get_lesson_count(self, obj):
        """
        Возвращает количество уроков в курсе.
        """
        return obj.lessons.count()
