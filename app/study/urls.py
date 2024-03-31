from django.urls import path
from .views import All_students_view,All_teachers_view,Course_view

urlpatterns = [
    path('students/',All_students_view.as_view(),name = 'students_all'),
    path('teachers/',All_teachers_view.as_view(),name = 'teachers_all'),
    path('courses/',Course_view.as_view(),name = 'courses'),
]
