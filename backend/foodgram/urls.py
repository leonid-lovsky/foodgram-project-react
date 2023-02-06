from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('api/', include('users.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('rest_framework.urls')), # TODO
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
