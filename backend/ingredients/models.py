from django.db.models import Model, CharField, UniqueConstraint
from django.utils.translation import gettext_lazy as _


class Ingredient(Model):
    name = CharField(
        _('название'),
        max_length=200,
        blank=False,
    )
    measurement_unit = CharField(
        _('единицы измерения'),
        max_length=200,
        blank=False,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            ),
        ]
