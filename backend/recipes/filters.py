from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import (
    BooleanFilter, FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter,
    NumberFilter
)
from tags.models import Tag

from .models import Recipe, RecipeFavorite, RecipeShoppingCart

User = get_user_model()


class RecipeFilter(FilterSet):
    is_favorited = BooleanFilter(
        label=_('Is favorited'),
        method='get_is_favorited',
    )
    is_in_shopping_cart = BooleanFilter(
        label=_('Is in shopping cart'),
        method='get_is_in_shopping_cart',
    )
    author = ModelChoiceFilter(
        queryset=User.objects.all(),
    )
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        label=_('Tags'),
    )

    def get_is_favorited(self, queryset, field_name, value):
        user = self.request.user
        if user.is_authenticated:
            # favorites_ids = (
            #     RecipeFavorite.objects.filter(user=user)
            #     .values('recipe_id')
            # )
            # return queryset.filter(pk__in=favorites_ids)
            return queryset.filter(
                recipefavorite__user=self.request.user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        user = self.request.user
        if user.is_authenticated:
            # recipes_in_shopping_cart_ids = (
            #     RecipeShoppingCart.objects.filter(user=user)
            #     .values('recipe_id')
            # )
            # return queryset.filter(pk__in=recipes_in_shopping_cart_ids)
            return queryset.filter(
                recipeshoppingcart__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'is_in_shopping_cart',
            'author',
            'tags',
        ]
