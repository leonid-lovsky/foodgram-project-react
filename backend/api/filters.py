from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from recipes import models as recipe_models

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(
        label=_('В избранном'),
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label=_('В корзине'),
        method='get_is_in_shopping_cart',
    )
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=recipe_models.Tag.objects.all(),
        field_name='tags__slug',
        label=_('Tags'),
    )

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        user = self.request.user
        return queryset.filter(
            recipeshoppingcart__user=user
        )

    def get_is_favorited(self, queryset, field_name, value):
        user = self.request.user
        return queryset.filter(
            recipefavorite__user=user
        )

    class Meta:
        model = recipe_models.Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]
