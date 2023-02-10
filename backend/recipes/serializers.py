from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Recipe


class RecipeSerializer(ModelSerializer):
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
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

    def get_is_favorited(self, obj):
        user = self.context.get('user')
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('user')
        return False
