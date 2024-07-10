from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UsersViewSet, PaymentsListAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register('users', UsersViewSet, basename='users')


urlpatterns = [path('payments/', PaymentsListAPIView.as_view(), name='payments-list'),
               path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               path('payment/', PaymentCreateAPIView.as_view(), name='create-pyment'),
               ] + router.urls
