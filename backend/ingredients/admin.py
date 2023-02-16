from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Ingredient


@admin.register(Ingredient)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'measurement_unit', 'get_usage']
    search_fields = ['name']

    def get_usage(self, obj):
        return obj.recipe_set.count()

    get_usage.short_description = _('Использований')
