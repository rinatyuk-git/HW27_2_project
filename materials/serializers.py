from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons_qty = serializers.SerializerMethodField()
    lessons_show = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lessons_qty(self, instance):
        if instance.lesson_set.all().count():
            return instance.lesson_set.all().count()
        return 0

    def get_lessons_show(self, course):
        return [lesson.lesson_name for lesson in Lesson.objects.filter(course=course)]
