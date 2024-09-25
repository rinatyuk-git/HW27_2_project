from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import (
    # UrlLessonValidator,
    validate_lesson_url)


class LessonSerializer(serializers.ModelSerializer):
    lesson_video = serializers.CharField(validators=[validate_lesson_url])

    class Meta:
        model = Lesson
        fields = "__all__"
        # validators = [UrlLessonValidator(field='lesson_video')]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, instance):
        return Subscription.objects.filter(
            user=self.context['request'].user,
            course_name=instance.pk).exists()

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_qty = serializers.SerializerMethodField()
    lessons_show = LessonSerializer(source='lesson_set', many=True)

    def get_lessons_qty(self, instance):
        if instance.lesson_set.all().count():
            return instance.lesson_set.all().count()
        return 0

    def get_lessons_show(self, course):
        return [lesson.lesson_name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = ("course_name", "course_description", "lessons_qty", "lessons_show",)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = "__all__"
