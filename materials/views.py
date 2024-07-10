from django.http import response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsUser
from materials.serialaizers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.permissions import IsModer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.course_owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny, ~IsModer,]
        if self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModer | IsUser]
        if self.action in ['update', 'partial_update', 'list', 'retrieve']:
            self.permission_classes = [IsAuthenticated | IsModer,]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer | IsUser]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.lesson_owner = self.request.user
        lesson.save()


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = MaterialsPagination
    permission_classes = [IsAuthenticated, IsModer | IsUser]


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsUser]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsUser]


class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModer | IsUser]


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subscription_item = Subscription.objects.filter(user=user, course=course_item)

        if subscription_item.exists():
            subscription_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item, active=True)
            message = 'подписка добавлена'
        return Response({"message": message})

