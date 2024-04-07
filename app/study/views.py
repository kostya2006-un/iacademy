import os
from django.http import Http404, FileResponse
from rest_framework import generics, viewsets, views, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Course, Subscription, Lesson, Application
from .serializer import Teacher_and_Student_serializer, CourseSerializer, SubscriptionSerializer, UserSerializer, AplicationSerializer, LessonSerializer
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
        course = serializer.validated_data['course']

        if course.closed:
            Application.objects.create(student=student,course=course)
        else:
            serializer.save(student = student)


class TeacherApplicationsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = request.user

        applications = Application.objects.filter(course__teacher=teacher)

        serializer = AplicationSerializer(applications, many=True)

        return Response(serializer.data)


class TeacherActivateView(views.APIView):
    permission_classes = [IsAuthenticated, Is_teacher_or_readonly]

    def get(self, request, aplication_id):
        try:
            application = Application.objects.get(id=aplication_id)
        except Application.DoesNotExist:
            return Response("Заявка не найдена", status=status.HTTP_404_NOT_FOUND)

        # Проверяем, является ли текущий пользователь учителем, у которого есть право активации заявок
        if not request.user == application.course.teacher:
            return Response("У вас нет прав для активации заявок", status=status.HTTP_403_FORBIDDEN)

        # Проверяем, что заявка еще не активирована
        if application.status:
            return Response("Заявка уже активирована", status=status.HTTP_400_BAD_REQUEST)

        # Устанавливаем статус заявки в True
        application.status = True
        application.save()

        # Создаем подписку на курс для студента
        existing_subscription = Subscription.objects.filter(student=application.student,
                                                            course=application.course).first()
        if existing_subscription:
            # Если подписка уже существует, просто обновляем ее статус
            existing_subscription.status = True
            existing_subscription.save()
            return Response("Подписка успешно активирована", status=status.HTTP_200_OK)
        else:
            # Если подписка не существует, создаем новую
            Subscription.objects.create(student=application.student, course=application.course)
            # Устанавливаем статус заявки в True
            application.status = True
            application.save()
            return Response("Заявка успешно активирована и студент записан на курс", status=status.HTTP_200_OK)


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


class LessonCourseView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        user = self.request.user

        if Subscription.objects.filter(student=user, course_id=course_id).exists():
            return Lesson.objects.filter(course_id=course_id)
        else:
            if Lesson.objects.filter(course_id=course_id, teacher=user).exists():
                return Lesson.objects.filter(course_id=course_id)
            else:
                raise PermissionDenied(
                    "You are not subscribed to this course and not a teacher of any lesson in this course.")


class LessonVideoView(views.APIView):

    def set_play(self,lesson):
        lesson.views += 1
        lesson.save()

    def get(self,request,pk):
        lesson = get_object_or_404(Lesson, id=pk)

        course_sub = Subscription.objects.filter(student = request.user, course = lesson.course)
        is_teacher = Lesson.objects.filter(course_id=lesson.course.id, teacher=request.user)
        if course_sub or is_teacher:
            if os.path.exists(lesson.video.path):
                self.set_play(lesson)
                return FileResponse(open(lesson.video.path, "rb"), filename=lesson.video.name)
            else:
                return Http404
        else:
            raise PermissionDenied("You don't have permission to watch this lesson.")

