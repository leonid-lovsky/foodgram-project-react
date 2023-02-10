from django.core.validators import RegexValidator
from django.db.models import CharField, Model, SlugField
from django.utils.translation import gettext_lazy as _

COLOR_VALIDATOR = RegexValidator(
    r'^#[a-fA-F0-9]{6}$',
    _('Используйте RGB-формат для указания цвета (#FFFFFF)'),
)


class Tag(Model):
    name = CharField(
        _('название'),
        max_length=200,
        unique=True,
        blank=False,
    )
    color = CharField(
        _('цвет'),
        max_length=7,
        validators=[
            COLOR_VALIDATOR,
        ],
        unique=True,
        blank=False,
    )
    slug = SlugField(
        _('slug'),
        max_length=200,
        unique=True,
        blank=False,
    )
