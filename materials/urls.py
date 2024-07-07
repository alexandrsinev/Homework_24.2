from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDeleteAPIView, SubscriptionAPIView

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
                  path('lesson/list/', LessonListAPIView.as_view(), name='lesson-list'),
                  path('lesson/detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-detail'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson-delete'),
                  path('subscription/', SubscriptionAPIView.as_view(), name='subscription-update'),
              ] + router.urls
