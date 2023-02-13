from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, SerializerMethodField
)

from .models import Recipe


class RecipeSerializer(ModelSerializer):
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        ]
        read_only_fields = [
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        ]

    def get_is_favorited(self, obj):
        # request = self.context["request"]
        # return (
        # request.user.is_authenticated
        # and recipe.favoriterecipe_set.filter(user=request.user).exists()
        # )
        user = self.context.get('user')
        return False

    def get_is_in_shopping_cart(self, obj):
        # request = self.context["request"]
        # return (
        # request.user.is_authenticated
        # and recipe.shoppingcartrecipe_set.filter(user=request.user).exists()
        # )
        user = self.context.get('user')
        return False


class RecipeCartSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]
        read_only_fields = [
            'name',
            'image',
            'cooking_time',
        ]
