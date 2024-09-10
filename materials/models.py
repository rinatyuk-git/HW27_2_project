"""
Курс:
название,
превью (картинка),
описание.

Урок:
название,
описание,
превью (картинка),
ссылка на видео.

Урок и курс - это связанные между собой сущности.
Уроки складываются в курс, в одном курсе может быть много уроков.
Реализуйте связь между ними.

"""
from django.db import models
NULLABLE = {"blank": True, "null": True}


class Lesson(models.Model):
    lesson_name = models.CharField(
        max_length=150,
        verbose_name='Название урока',
    )  # Наименование урока
    lesson_description = models.TextField(
        max_length=1255,
        verbose_name="Информация об уроке",
        **NULLABLE,
    )  # Описание урока
    course_preview = models.ImageField(
        upload_to="lessons/images",
        verbose_name="Изображение для урока",
        **NULLABLE,
    )  # Изображение (превью)
    lesson_video = models.URLField(
        max_length=2000,
        verbose_name="Видео для урока",
    )  # ссылка на видео

    def __str__(self):
        return f'{self.lesson_name}'

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Course(models.Model):
    course_name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
    )  # Наименование курса
    lessons = models.ManyToManyField(
        Lesson,
        verbose_name="Уроки",
        help_text="Выберите урок",
        related_name="courses",
        # **NULLABLE,
    )  # уроки в курсе
    course_preview = models.ImageField(
        upload_to="courses/images",
        verbose_name="Изображение для курса",
        **NULLABLE,
    )  # Изображение (превью)
    course_description = models.TextField(
        max_length=1255,
        verbose_name="Информация о курсе",
        **NULLABLE,
    )  # Описание курса

    def __str__(self):
        return f'{self.course_name}'

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
