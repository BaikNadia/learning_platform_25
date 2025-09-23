from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    preview = models.ImageField(upload_to='courses/previews/', verbose_name="Превью", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="owned_courses"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    preview = models.ImageField(upload_to='lessons/previews/', verbose_name="Превью", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name="Курс"
    )
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="owned_lessons"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
