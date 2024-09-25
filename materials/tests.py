from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.test")
        self.course = Course.objects.create(
            course_name="course_name_test",
            course_description="course_description_test",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            lesson_name="lesson_name_test",
            lesson_description="lesson_description_test",
            lesson_video="https://www.youtube.com/cs/fotky/car-paris",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse('materials:lesson-create')
        data = {
            "lesson_name": "lesson_name_test",
            "lesson_description": "lesson_description_test",
            "lesson_video": "https://www.youtube.com/cs/fotky/car-paris"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {'id': self.lesson.pk,
                 'lesson_video': self.lesson.lesson_video,
                 'lesson_name': self.lesson.lesson_name,
                 'lesson_description': self.lesson.lesson_description,
                 'lesson_preview': None,
                 'course': self.course.pk,
                 'owner': self.user.pk}
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )

    def test_lesson_retrieve(self):
        url = reverse('materials:lesson-detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('lesson_name'), self.lesson.lesson_name
        )

    def test_lesson_update(self):
        url = reverse('materials:lesson-update', args=(self.lesson.pk,))
        data = {
            "lesson_name": "lesson_name_test",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get('lesson_name'), "lesson_name_test"
        )

    def test_lesson_delete(self):
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.test")
        self.course = Course.objects.create(
            course_name="course_name_test",
            course_description="course_description_test",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            lesson_name="lesson_name_test",
            lesson_description="lesson_description_test",
            lesson_video="https://www.youtube.com/cs/fotky/car-paris",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('materials:subs_create')
        data = {
            "course_name": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)
        ans = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all().count(), 1
        )
        self.assertEqual(
            ans.get('message'), "подписка добавлена"
        )

    def test_subscription_delete(self):
        Subscription.objects.create(user=self.user, course_name=self.course)
        url = reverse('materials:subs_create')
        data = {
            "course_name": self.course.id,
            "user": self.user.id,
        }
        response = self.client.post(url, data=data)
        ans = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Subscription.objects.all().count(), 0
        )
        self.assertEqual(
            ans.get('message'), "подписка удалена"
        )
