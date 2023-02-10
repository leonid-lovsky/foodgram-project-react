from common.permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import permissions, viewsets
from djoser.views import UserViewSet
from common.pagination import PageLimitPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pass
