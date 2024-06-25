from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    number_lessons = SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    def get_number_lessons(self, instance):
        return instance.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ('title', 'description', 'number_lessons', 'lessons')
