from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'users'  # TODO

router = DefaultRouter()

urlpatterns = [
    # path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken'))
]
