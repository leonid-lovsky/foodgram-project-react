from collections import defaultdict
from django.http import HttpResponse

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
from .models import Recipe, RecipeFavorite, RecipeIngredient, RecipeShoppingCart
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
        recipe_user = model.objects.create(recipe=recipe, user=user)
        serializer = RecipeShortSerializer(recipe_user)
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
        user = request.user
        shopping_carts = RecipeShoppingCart.objects.filter(user=user).all()
        shopping_list = defaultdict(int)

        for shopping_cart in shopping_carts:
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe=shopping_cart.recipe
            ).all()

            for recipe_ingredient in recipe_ingredients:
                shopping_list[
                    (
                        recipe_ingredient.ingredient.name,
                        recipe_ingredient.ingredient.measurement_unit,
                    )
                ] += recipe_ingredient.amount

        output = 'Список покупок:\n'
        for key, value in shopping_list.items():
            output += f'* {key[0]} ({key[1]}) — {value}\n'

        file_name = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file_name}.txt"'
        return response
