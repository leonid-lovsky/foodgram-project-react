from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        _('название'),
        max_length=150,
    )
    image = models.ImageField(
        _('картинка'),
        upload_to='recipes',
    )
    text = models.TextField(
        _('описание'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
    )
    cooking_time = models.IntegerField(
        _('время приготовления'),
        validators=[
            MinValueValidator(1),
        ],
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(
        _('количество'),
        validators=[
            MinValueValidator(1),
        ],
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.RESTRICT,
    )
