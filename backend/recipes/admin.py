from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time',
                    'get_ingredients', 'get_favorites', 'get_shopping_carts']
    search_fields = ['author', 'name']
    # TODO: list filter name
    list_filter = ['tags']
    # TODO: inline models
    filter_horizontal = ['tags']
    # filter_horizontal = ['ingredients']
    # inlines = ['TagInline']
    # inlines = ['IngredientInline']

    def get_ingredients(self, obj):
        return obj.recipeingredient_set.count()

    get_ingredients.short_description = _('Ингредиентов')


    def get_favorites(self, obj):
        return obj.recipefavorite_set.count()

    get_favorites.short_description = _('В избранном')

    def get_shopping_carts(self, obj):
        return obj.recipeshoppingcart_set.count()

    get_shopping_carts.short_description = _('В корзине')


