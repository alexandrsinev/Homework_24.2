from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Users, Payments

from users.serializers import UserSerializer, PaymentSerializer
from users.services import create_price, create_stripe_sessions, create_stripe_product


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsListAPIView(ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    ordering_fields = ('date_of_payment',)
    permission_classes = [IsAuthenticated, ]


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        payment = serializer.save(user=self.request.user)
        print(serializer)
        print(payment)
        print(payment.paid_course)
        product = create_stripe_product(payment.paid_course)
        price = create_price(product=product, payment_amount=payment.payment_amount)
        session_id, payment_link = create_stripe_sessions(price)
        payment.id_session = session_id
        payment.link = payment_link
        payment.save()
