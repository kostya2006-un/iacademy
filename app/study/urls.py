from django.urls import path
from .views import All_students_view,All_teachers_view,Course_view,CourseRetrieveUpdateView,CourseAll

urlpatterns = [
    path('students/',All_students_view.as_view(),name = 'students_all'),
    path('teachers/',All_teachers_view.as_view(),name = 'teachers_all'),
    path('courses_create/',Course_view.as_view(),name = 'courses_create'),
    path('teacher_courses/<int:pk>/',CourseRetrieveUpdateView.as_view(),name = 'teacher_courses'),
    path('courses/',CourseAll.as_view(), name = 'courses')

]
