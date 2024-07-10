from rest_framework.serializers import ModelSerializer

from users.models import Users, Payments


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payment_history = PaymentSerializer(
        source="user_payment", many=True, read_only=True
    )

    class Meta:
        model = Users
        fields = '__all__'
