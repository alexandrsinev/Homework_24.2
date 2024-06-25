from rest_framework.serializers import ModelSerializer

from users.models import Users, Payments


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ('first_name', 'email',)


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
