import base64
import uuid

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser import serializers as djoser_serializers
from rest_framework import serializers

from recipes.models import (
    Subscription, IngredientInRecipe, Tag, Recipe, TagRecipe,
    RecipeInShoppingCart, FavoriteRecipe, Ingredient,
)

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            file_name = str(uuid.uuid4())
            file_extension = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name=file_name + '.' + file_extension
            )

        return super().to_internal_value(data)


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        ]


class UserSerializer(djoser_serializers.UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_anonymous:
            return False
        queryset = Subscription.objects.all()
        return queryset.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        source='ingredientrecipe_set',
        many=True, read_only=True,
    )

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

    @staticmethod
    def create_recipe_tags(recipe, tags_ids):
        recipe_tags = [
            TagRecipe(
                recipe=recipe,
                tag_id=tag_id,
            )
            for tag_id in tags_ids
        ]
        TagRecipe.objects.bulk_create(recipe_tags)

    @staticmethod
    def create_ingredients_in_recipe(recipe, ingredients_data):
        ingredients_in_recipe = [
            IngredientInRecipe(
                recipe=recipe,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount'),
            )
            for ingredient_data in ingredients_data
        ]
        IngredientInRecipe.objects.bulk_create(ingredients_in_recipe)

    def create(self, validated_data):
        instance = super().create(validated_data)
        tags_ids = self.initial_data.get('tags')
        ingredients_data = self.initial_data.get('ingredients')
        self.create_recipe_tags(instance, tags_ids)
        self.create_ingredients_in_recipe(instance, ingredients_data)
        return instance

    def update(self, instance, validated_data):
        TagRecipe.objects.filter(recipe=instance).delete()
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        instance = super().update(instance, validated_data)
        tags_ids = self.initial_data.get('tags')
        ingredients_data = self.initial_data.get('ingredients')
        self.create_recipe_tags(instance, tags_ids)
        self.create_ingredients_in_recipe(instance, ingredients_data)
        return instance

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_anonymous:
            return False
        queryset = RecipeInShoppingCart.objects.all()
        return queryset.filter(recipe=obj, user=user).exists()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_anonymous:
            return False
        queryset = FavoriteRecipe.objects.all()
        return queryset.filter(recipe=obj, user=user).exists()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class UserWithRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_anonymous:
            return False
        return Subscription.objects.filter(user=user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return ShortRecipeSerializer(queryset, many=True).data

    # noinspection PyMethodMayBeStatic
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]
