from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.viewsets import ModelViewSet

from common.pagination import PageLimitPagination
from common.permissions import IsAuthorOrReadOnly

from .filters import RecipeFilter
from .models import Recipe, RecipeCart
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
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
        methods=[
            'post',
            'delete',
        ],
        url_path='shopping_cart',
        permission_classes=[
            IsAuthenticated
        ]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            RecipeCart.objects.create(
                recipe=recipe,
                user=user,
            )
        if request.method == 'DELETE':
            item = RecipeCart.objects.filter(
                recipe=recipe,
                user=user,
            )
            if not item.exists():
                raise Http404
            item.delete()