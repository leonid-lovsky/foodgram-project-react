from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)
from rest_framework.viewsets import ModelViewSet

from common.pagination import PageLimitPagination
from common.permissions import IsAuthorOrReadOnly

from .filters import RecipeFilter
from .models import Recipe, RecipeShoppingCart, RecipeFavorite
from .serializers import RecipeSerializer, RecipeShortSerializer


class RecipeMixin():
    def custom_action(self, request, model, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        item = model.objects.filter(
            recipe=recipe,
            user=user,
        )

        if request.method == 'POST':
            if item.exists():
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )

            model.objects.create(
                recipe=recipe,
                user=user,
            )
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            if not item.exists():
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )

            item.delete()
            return Response(
                status=HTTP_204_NO_CONTENT
            )


class RecipeViewSet(ModelViewSet, RecipeMixin):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        self.custom_action(request, RecipeShoppingCart, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        self.custom_action(request, RecipeFavorite, pk)
