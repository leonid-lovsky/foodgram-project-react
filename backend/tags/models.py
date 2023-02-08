from django.db import models
from django.core.validators import RegexValidator

from django.utils.translation import gettext_lazy as _

COLOR_VALIDATOR = RegexValidator(
    r'^#[a-fA-F0-9]{6}$',
    _('Используйте RGB-формат для указания цвета (#FFFFFF)'),
)


class Tag(models.Model):
    name = models.CharField(
        _('название'),
        max_length=50,
        blank=False,
        unique=True,
    )
    color = models.CharField(
        _('цвет'),
        max_length=50,
        validators=[
            COLOR_VALIDATOR,
        ],
        blank=False,
        unique=True,
    )
    slug = models.SlugField(
        _('slug'),
        max_length=50,
        blank=False,
        unique=True,
    )
