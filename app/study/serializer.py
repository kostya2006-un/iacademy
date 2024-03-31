from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Course


User = get_user_model()


class Teacher_and_Student_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "ava")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ['teacher']