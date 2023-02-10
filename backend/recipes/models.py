from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, RESTRICT, CharField, ForeignKey,
                              ImageField, IntegerField, ManyToManyField, Model,
                              TextField)
from django.utils.translation import gettext_lazy as _
from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(Model):
    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name='recipes',
    )
    name = CharField(
        _('название'),
        max_length=200,
    )
    image = ImageField(
        _('картинка'),
        upload_to='recipes',
    )
    text = TextField(
        _('описание'),
    )
    ingredients = ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
    )
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        through='RecipeTag',
    )
    cooking_time = IntegerField(
        _('время приготовления'),
        validators=[
            MinValueValidator(1),
        ],
    )


class RecipeIngredient(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    ingredient = ForeignKey(
        Ingredient,
        on_delete=RESTRICT,
    )
    amount = IntegerField(
        _('количество'),
        validators=[
            MinValueValidator(1),
        ],
    )


class RecipeTag(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    tag = ForeignKey(
        Tag,
        on_delete=RESTRICT,
    )
