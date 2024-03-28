from django.urls import path, re_path, include

urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'', include('djoser.urls.authtoken')),
]
