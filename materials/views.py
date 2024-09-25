from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from materials.models import Course, Lesson, Subscription
from materials.paginators import PagePaginator
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   CourseDetailSerializer, SubscriptionSerializer
                                   )
from users.permissions import (
    IsOwner,
    IsModerator
)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated | ~IsModerator,)
    # permission_classes = (~IsModerator,)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = PagePaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsModerator | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [~IsModerator | IsOwner]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = PagePaginator

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModerator,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerator | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerator | IsOwner,)
        return super().get_permissions()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Subscription.objects.all()

    def post(self, *args, **kwargs):
        user = self.request.user  # получаем пользователя из self.requests
        course_id = self.request.data.get("course_name") # получаем id курса из self.requests.data
        course_item = get_object_or_404(Course, pk=course_id)  # получаем объект курса из базы с помощью get_object_or_404
        subs_item = Subscription.objects.filter(user=user, course_name=course_item)  # получаем объекты подписок по текущему пользователю и курсу

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course_name=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    pagination_class = PagePaginator
    queryset = Subscription.objects.all()
