from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import URLValidator


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [URLValidator(field='url')]


class CourseSerializer(ModelSerializer):
    number_lessons = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = SerializerMethodField(read_only=True)

    def get_number_lessons(self, instance):
        return instance.lesson_set.all().count()

    def get_subscription(self, instance):
        request = self.context.get('request')
        user = None
        if request:
            user = request.user
            return instance.subscription_set.filter(user=user).exists()

    class Meta:
        model = Course
        fields = ('title', 'description', 'subscription', 'number_lessons', 'lessons')
