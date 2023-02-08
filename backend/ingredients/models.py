from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    name = models.CharField(
        _('название'),
        max_length=150
    )
    measurement_unit = models.CharField(
        _('единицы измерения'),
        max_length=25,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            ),
        ]
