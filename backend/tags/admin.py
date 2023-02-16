from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Tag


@admin.register(Tag)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'slug', 'get_usage']

    def get_usage(self, obj):
        return obj.recipe_set.count()

    get_usage.short_description = _('Использований')
