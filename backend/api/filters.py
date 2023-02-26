from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from recipes.models import Tag, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        label=_('В избранном'),
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label=_('В корзине'),
        method='get_is_in_shopping_cart'
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label=_('Теги'),
        field_name='tags__slug',
        to_field_name='slug'
    )

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]

    def get_is_favorited(self, queryset, field_name, value):
        user = self.request.user
        # if user and user.is_authenticated:
        return queryset.filter(
            favoriterecipe__user=user
        )
        # return queryset

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        user = self.request.user
        # if user and user.is_authenticated:
        return queryset.filter(
            recipeinshoppingcart__user=user
        )
        # return queryset
