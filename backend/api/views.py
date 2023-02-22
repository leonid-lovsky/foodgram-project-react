from collections import defaultdict

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser import views as djoser_views
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.models import *

from .filters import *
from .pagination import *
from .permissions import *
from .serializers import *

User = get_user_model()


class UserViewSet(djoser_views.UserViewSet):
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        subscriptions = User.objects.filter(
            subscribers__user=self.request.user
        )
        context = {'request': request}
        serializer = UserWithRecipesSerializer(
            subscriptions, many=True, context=context
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, pk=id)
        context = {'request': request}
        if request.method == 'POST':
            try:
                instance = Subscription.objects.create(
                    author=author, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = UserWithRecipesSerializer(
                instance.author, context=context
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                instance = Subscription.objects.get(
                    author=author, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly,
    ]
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        recipes_in_shopping_cart = RecipeInShoppingCart.objects.filter(
            user=self.request.user
        ).all()
        shopping_list = defaultdict(int)

        for recipe_in_shopping_cart in recipes_in_shopping_cart:
            ingredients_in_recipe = IngredientInRecipe.objects.filter(
                recipe=recipe_in_shopping_cart.recipe
            ).all()

            for ingredient_in_recipe in ingredients_in_recipe:
                shopping_list[
                    (
                        ingredient_in_recipe.ingredient.name,
                        ingredient_in_recipe.ingredient.measurement_unit,
                    )
                ] += ingredient_in_recipe.amount

        output = 'Список покупок:\n'
        for key, value in shopping_list.items():
            output += f'* {key[0]} ({key[1]}) — {value}\n'

        file_name = 'shopping_list'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="{file_name}.txt"'
        )
        return response

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            try:
                instance = RecipeInShoppingCart.objects.create(
                    recipe=recipe, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            context = {'request': self.request}
            serializer = ShortRecipeSerializer(
                instance.recipe, context=context
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                instance = RecipeInShoppingCart.objects.get(
                    recipe=recipe, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            try:
                instance = FavoriteRecipe.objects.create(
                    recipe=recipe, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            context = {'request': self.request}
            serializer = ShortRecipeSerializer(
                instance.recipe, context=context
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                instance = FavoriteRecipe.objects.get(
                    recipe=recipe, user=self.request.user
                )
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
