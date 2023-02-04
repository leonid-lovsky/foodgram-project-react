from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'  # TODO

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
