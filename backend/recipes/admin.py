from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Recipe, RecipeIngredient, RecipeTag


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time',
                    'get_ingredient_count', 'get_favorite_count',
                    'get_shopping_cart_count']
    search_fields = ['author', 'name']
    list_filter = ['tags']

    inlines = [IngredientInline, TagInline]

    def get_ingredient_count(self, obj):
        return obj.recipeingredient_set.count()

    get_ingredient_count.short_description = _('Ингредиентов')

    def get_favorite_count(self, obj):
        return obj.recipefavorite_set.count()

    get_favorite_count.short_description = _('В избранном')

    def get_shopping_cart_count(self, obj):
        return obj.recipeshoppingcart_set.count()

    get_shopping_cart_count.short_description = _('В корзине')
