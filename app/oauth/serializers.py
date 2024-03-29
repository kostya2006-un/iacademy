from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUser
from .services import delete_old_ava_path
User = get_user_model()


class CustomUserSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ("email","first_name","last_name","password","is_teacher")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','first_name', 'last_name','ava','username', 'is_teacher']
        read_only_fields = ['email','first_name', 'last_name','is_teacher']

    def update(self, instance, validated_data):
        delete_old_ava_path(instance.ava.path)
        return super().update(instance,validated_data)