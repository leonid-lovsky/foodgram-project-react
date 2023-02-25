from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from recipes.models import Tag, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    is_favorite = filters.BooleanFilter(
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

    class Meta:
        model = Recipe
        fields = [
            'is_favorite',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]

    def get_is_favorite(self, queryset):
        return queryset.filter(
            favoriterecipe__user=self.request.user
        )

    def get_is_in_shopping_cart(self, queryset):
        return queryset.filter(
            shoppingcartrecipe__user=self.request.user
        )
