from django.urls import reverse

from materials.models import Course, Lesson, Subscription
from users.models import Users
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Users


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(email="admin@test.com")
        self.course = Course.objects.create(
            title="CourseTest", description="CourseTest description", course_owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title_lesson="LessonTest",
            description="LessonTest description",
            course=self.course,
            lesson_owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_course(self):
        """ Тестирование CRUD курса"""
        create_data = {
            "title": "Швея",
            "description": "Описание курса Швея",
            "lessons": []
        }

        response = self.client.post('', data=create_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = Users.objects.create(email="admin@test.com")
        self.course = Course.objects.create(
            title="CourseTest", description="CourseTest description", course_owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title_lesson="LessonTest",
            description="LessonTest description",
            course=self.course,
            lesson_owner=self.user,
            url='https://www.youtube.com/',
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "New Lesson",
            "description": "New Lesson description",
            "course": self.course.pk,
            "url": "https://www.youtube.com/",
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title_lesson": self.lesson.title_lesson,
                    "preview": None,
                    "description": self.lesson.description,
                    "url": 'https://www.youtube.com/',
                    "course": self.course.pk,
                    "lesson_owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title_lesson"], self.lesson.title_lesson)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title_lesson": "New Test Lesson"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title_lesson"], "New Test Lesson")

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = Users.objects.create(email="admin@test.com")
        self.course = Course.objects.create(
            title="CourseTest", description="CourseTest description", course_owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("materials:subscription-update")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "подписка добавлена"})

    def test_unsubscribe(self):
        url = reverse("materials:subscription-update")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "подписка удалена"})
