from collections import defaultdict

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.viewsets import *

from ingredients.models import *
from recipes.models import *
from tags.models import *
from users.models import *

from .filters import *
from .pagination import *
from .permissions import *
from .serializers import *

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


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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
