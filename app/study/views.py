from rest_framework import generics
from .serializer import Teacher_and_Student_serializer
from django.contrib.auth import get_user_model

User = get_user_model()


class All_students_view(generics.ListAPIView):
    serializer_class = Teacher_and_Student_serializer

    def get_queryset(self):
        return User.objects.filter(is_teacher = False)


class All_teachers_view(generics.ListAPIView):
    serializer_class = Teacher_and_Student_serializer

    def get_queryset(self):
        return User.objects.filter(is_teacher = True)