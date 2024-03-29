from django.urls import path, re_path, include
from .views import ProfileApiView

urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include('djoser.urls.authtoken')),
    path('profile/', ProfileApiView.as_view(),name = 'profile_api'),
]
