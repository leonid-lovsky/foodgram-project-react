from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns = [
    path('api/', include('users.urls')),  # TODO
]

urlpatterns += [
    path('auth/', include('rest_framework.urls')),  # TODO
]

# TODO
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.STATIC_URL,
#         document_root=settings.STATIC_ROOT
#     )

#     urlpatterns += static(
#         settings.MEDIA_URL,
#         document_root=settings.MEDIA_ROOT
#     )
