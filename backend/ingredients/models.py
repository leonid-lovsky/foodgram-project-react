from django.db.models import Model, CharField, UniqueConstraint
from django.utils.translation import gettext_lazy as _


class Ingredient(Model):
    name = CharField(
        _('Название'),
        max_length=200,
        blank=False,
    )
    measurement_unit = CharField(
        _('Единицы измерения'),
        max_length=200,
        blank=False,
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]
    
    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'
