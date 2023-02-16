from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time', 'get_favorites']
    search_fields = ['author', 'name']
    list_filter = ['tags']
    # filter_horizontal = ['ingredients', 'tags']
    filter_horizontal = ['tags']

    def get_favorites(self, obj):
        return obj.recipefavorite_set.count()

    get_favorites.short_description = 'Популярнсть'
