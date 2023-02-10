from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from recipes.views import RecipeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('auth/', include('rest_framework.urls'))
]

# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT
#     )

#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )
