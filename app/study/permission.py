from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class Is_teacher_or_readonly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_teacher
        return False


class Is_Owner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.teacher == request.user:
            return True
        return False
