from django.urls import include, path

from . import views

urlpatterns = [
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken'))
]
