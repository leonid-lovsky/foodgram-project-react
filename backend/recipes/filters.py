from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import (
    BooleanFilter, FilterSet, ModelChoiceFilter, ModelMultipleChoiceFilter,
    NumberFilter
)
from tags.models import Tag

from .models import Recipe

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
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                # favorites__user=self.request.user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, field_name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(
                # cart__user=self.request.user
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
