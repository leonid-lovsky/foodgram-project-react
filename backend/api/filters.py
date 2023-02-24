from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from recipes.models import *

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        label=_('В избранном'),
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label=_('В корзине'),
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        label=_('Tags'),
        field_name='tags__slug',
    )

    def get_is_favorited(self, queryset, field_name, value):
        return queryset.filter(
            favoriterecipe__user=self.request.user
        )

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        return queryset.filter(
            shoppingcartrecipe__user=self.request.user
        )

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]
