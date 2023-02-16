from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'cooking_time', 'get_favorites']
    search_fields = ['author', 'name']
    list_filter = ['tags']
    filter_horizontal = ['tags']
    # filter_horizontal = ['ingredients', 'tags']

    def get_favorites(self, obj):
        return obj.recipefavorite_set.count()

    get_favorites.short_description = _('Популярнсть')
