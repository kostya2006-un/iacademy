from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Course, Subscription, Lesson
from .serializer import Teacher_and_Student_serializer, CourseSerializer, SubscriptionSerializer, UserSerializer, \
    LessonSerializer
from django.contrib.auth import get_user_model
from .permission import Is_teacher_or_readonly,Is_Owner

User = get_user_model()


class All_students_view(generics.ListAPIView):
    serializer_class = Teacher_and_Student_serializer

    def get_queryset(self):
        return User.objects.filter(is_teacher = False)


class All_teachers_view(generics.ListAPIView):
    serializer_class = Teacher_and_Student_serializer

    def get_queryset(self):
        return User.objects.filter(is_teacher = True)


class Course_view(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,Is_teacher_or_readonly, ]

    def get_queryset(self):
        return Course.objects.filter(teacher = self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated or not self.request.user.is_teacher:
            raise PermissionDenied("У вас нет прав на создание курса")
        serializer.save(teacher=self.request.user)


class CourseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [Is_Owner, ]


class CourseAll(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class SubscriptionCreateView(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(student = self.request.user)

    def perform_create(self, serializer):
        student = self.request.user

        serializer.save(student = student)


class CourseSubscriptionView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        course_id = self.kwargs["course_id"]

        course = Course.objects.get(id = course_id)

        students = course.subscriptions.all().select_related('student').values('student')
        return User.objects.filter(id__in=students)


class LessonTeacherView(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [Is_Owner,Is_teacher_or_readonly,IsAuthenticated, ]

    def get_queryset(self):
        return Lesson.objects.filter(teacher = self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher = self.request.user)