from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from common.pagination import PageLimitPagination
from common.permissions import IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly

from .filters import RecipeFilter
from .models import Recipe, RecipeFavorite, RecipeShoppingCart
from .serializers import RecipeSerializer, RecipeShortSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        self.new_create_or_delete(RecipeShoppingCart, request, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        self.new_create_or_delete(RecipeFavorite, request, pk)

    def custom_create_or_delete_action(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            self.create_recipe(model, recipe, request.user)
        if request.method == 'DELETE':
            self.delete_recipe(model, recipe, request.user)

    def custom_create_action(self, model, recipe, user):
        item = model.objects.create(recipe=recipe, user=user)
        serializer = RecipeShortSerializer(item)
        return Response(serializer.data, status=HTTP_201_CREATED)

    def custom_delete_action(self, model, recipe, user):
        model.objects.filter(recipe=recipe, user=user).delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        RecipeShoppingCart.objects.filter(user=request.user)
