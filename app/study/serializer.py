from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Course,Subscription,Lesson
from .services import delete_old_video_path

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name")


class Teacher_and_Student_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "ava")


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['teacher']


class SubscriptionSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ['student']


class LessonSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ("__all__")
        read_only_fields = ['teacher','views']

    def update(self, instance, validated_data):
        delete_old_video_path(instance.video.path)
        return super().update(instance, validated_data)
