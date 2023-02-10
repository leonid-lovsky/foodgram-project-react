from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

from common.pagination import PageLimitPagination
User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6
