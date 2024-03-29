from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ("email","first_name","last_name","password","is_teacher")