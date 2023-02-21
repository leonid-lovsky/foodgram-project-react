import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser import serializers as djoser_serializers
from rest_framework import serializers

from recipes.models import *

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class WriteUserSerializer(djoser_serializers.UserCreateSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]


class ReadUserSerializer(djoser_serializers.UserSerializer):
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
        if user and user.is_authenticated:
            return Subscription.objects.filter(
                user=user, author=obj
            ).exists()
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'name',
            'color',
            'slug',
        ]


class WriteRecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = serializers.PrimaryKeyRelatedField(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        ]

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        for tag in tags:
            # recipe.tags.add(tag)
            tag = TagRecipe.objects.create(
                recipe=recipe,
                tag_id=tag,
            )
        for ingredient in ingredients:
            ingredient = IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            # recipe.ingredients.add(ingredient)
        return recipe


class ReadRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    image = Base64ImageField()

    author = ReadUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True, read_only=True,
    )

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
        ]

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_authenticated:
            return ShoppingCartRecipe.objects.filter(
                recipe=obj, user=user
            ).exists()
        return False

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user and user.is_authenticated:
            return FavoriteRecipe.objects.filter(
                recipe=obj, user=user
            ).exists()
        return False

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        for tag in tags:
            # recipe.tags.add(tag)
            tag = TagRecipe.objects.create(
                recipe=recipe,
                tag_id=tag,
            )
        for ingredient in ingredients:
            ingredient = IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            # recipe.ingredients.add(ingredient)
        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = [
            'id',
            'name',
            'measurement_unit',
            'amount',
        ]


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = [
            'id',
            'name',
            'image',
            'cooking_time',
        ]


class AuthorWithRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

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
        if user and user.is_authenticated:
            return Follow.objects.filter(
                user=user, author=obj
            ).exists()
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
