from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "course_name",
    )


@admin.register(Lesson)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lesson_name",
    )