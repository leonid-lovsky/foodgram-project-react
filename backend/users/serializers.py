from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, SerializerMethodField
)

from recipes.models import Recipe
from recipes.serializers import RecipeShortSerializer

from .models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(
        method_name='get_is_subscribed'
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
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        return Subscription.objects.filter(
            user=user, author=obj,
        ).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
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


class AuthorWithRecipesSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = SerializerMethodField(
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
        return Subscription.objects.filter(
            user=user, author=obj,
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(
            author=obj,
        ).count()
