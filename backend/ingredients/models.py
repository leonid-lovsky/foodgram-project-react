from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    name = models.CharField(
        _('название'),
        max_length=150,
        blank=False,
    )
    measurement_unit = models.CharField(
        _('единицы измерения'),
        max_length=25,
        blank=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique ingredient'
            ),
        ]
