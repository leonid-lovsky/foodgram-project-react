from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, SerializerMethodField
)

from .models import Recipe, RecipeShoppingCart, RecipeFavorite


class RecipeSerializer(ModelSerializer):
    is_favorited = SerializerMethodField(
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = SerializerMethodField(
        method_name='get_is_in_shopping_cart'
    )

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
        request = self.context.get('request')
        user = request.user
        return RecipeFavorite.objects.filter(
            recipe=obj,
            user=user
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        return RecipeShoppingCart.objects.filter(
            recipe=obj,
            user=user
        ).exists()


class RecipeShortSerializer(ModelSerializer):
    image = Base64ImageField()

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
