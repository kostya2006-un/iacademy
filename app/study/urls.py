from django.urls import path
from .views import All_students_view,All_teachers_view,Course_view,CourseRetrieveUpdateView,CourseAll,SubscriptionCreateView
from .views import CourseSubscriptionView,LessonTeacherView,LessonCourseView,LessonVideoView

urlpatterns = [
    path('students/',All_students_view.as_view(),name = 'students_all'),
    path('teachers/',All_teachers_view.as_view(),name = 'teachers_all'),
    path('courses_create/',Course_view.as_view(),name = 'courses_create'),
    path('teacher_courses/<int:pk>/',CourseRetrieveUpdateView.as_view(),name = 'teacher_courses'),
    path('courses/',CourseAll.as_view(), name = 'courses'),
    path('courses/<int:pk>/', LessonCourseView.as_view(), name='course-lessons'),
    path('lessons/video/<int:pk>/', LessonVideoView.as_view(), name='lesson-video'),
    path('subscription/',SubscriptionCreateView.as_view(),name = 'subscription'),
    path('courses/<int:course_id>/students/', CourseSubscriptionView.as_view(), name='course_students_list'),
    path('lessons_my/', LessonTeacherView.as_view({'get':'list','post':'create'})),
    path('lessons_my/<int:pk>/', LessonTeacherView.as_view({'put':'update','delete':'destroy'})),
]
