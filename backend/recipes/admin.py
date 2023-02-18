from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit', 'get_usage']
    search_fields = ['name']

    def get_usage(self, obj):
        return obj.recipe_set.count()

    get_usage.short_description = _('Использований')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug', 'get_usage']

    def get_usage(self, obj):
        return obj.recipe_set.count()

    get_usage.short_description = _('Использований')


class IngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1


class TagInline(admin.TabularInline):
    model = models.RecipeTag
    extra = 1


class ShoppingCartInline(admin.TabularInline):
    model = models.RecipeShoppingCart
    extra = 1


class FavoriteInline(admin.TabularInline):
    model = models.RecipeFavorite
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'author',
        'cooking_time',
        'get_ingredient_count',
        'get_shopping_cart_count',
        'get_favorite_count',
    ]
    search_fields = [
        'author',
        'name',
    ]
    list_filter = ['tags']

    inlines = [IngredientInline, TagInline, ShoppingCartInline, FavoriteInline]

    def get_ingredient_count(self, obj):
        return obj.recipeingredient_set.count()

    get_ingredient_count.short_description = _('Ингредиентов')

    def get_shopping_cart_count(self, obj):
        return obj.recipeshoppingcart_set.count()

    get_shopping_cart_count.short_description = _('В корзине')

    def get_favorite_count(self, obj):
        return obj.recipefavorite_set.count()

    get_favorite_count.short_description = _('В избранном')
