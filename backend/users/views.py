from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)

from common.pagination import PageLimitPagination

from .models import Subscription
from .serializers import AuthorWithRecipesSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request, pk=None):
        following = self.get_queryset().filter(follow__user=request.user)
        serializer = AuthorWithRecipesSerializer(following)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            Subscription.objects.create(author=author, user=request.user)
            serializer = AuthorWithRecipesSerializer(author)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if request.method == 'DELETE':
            Subscription.objects.filter(
                author=author, user=request.user
            ).delete()
            return Response(status=HTTP_204_NO_CONTENT)
