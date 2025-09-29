from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link


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
            'course',
        ]

        read_only_fields = ('owner',)

    def get_fields(self):
        """
        Убираем поле video_url из read_only при создании/обновлении,
        но оставляем его обязательным и валидируемым.
        """
        fields = super().get_fields()
        # Можно добавить дополнительные настройки при необходимости
        return fields

    # Применяем валидатор к полю video_url
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['video_url'].validators.append(validate_youtube_link)


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курс.
    Включает:
    - lesson_count — количество уроков
    - lessons — список всех уроков курса
    - is_subscribed — подписан ли текущий пользователь
    """
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'preview',
            'owner',
            'lesson_count',
            'lessons',
            'is_subscribed',
        ]
        read_only_fields = ('owner',)

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=request.user, course=obj).exists()
