import django
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE, RESTRICT, CharField, DateTimeField, ForeignKey, ImageField,
    IntegerField, ManyToManyField, Model, TextField, UniqueConstraint
)
from django.utils.translation import gettext_lazy as _

from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(Model):
    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name=_('Автор'),
    )
    name = CharField(
        _('Название'),
        max_length=200,
    )
    image = ImageField(
        _('Картинка'),
        upload_to='recipes/images',
    )
    text = TextField(
        _('Описание'),
    )
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name=_('Ингредиенты'),
    )
    tags = ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name=_('Теги'),
    )
    cooking_time = IntegerField(
        _('Время приготовления'),
        validators=[
            MinValueValidator(1),
        ],
    )
    pub_date = DateTimeField(
        _('Дата публикации'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}'


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
        _('Количество'),
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class RecipeTag(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    tag = ForeignKey(
        Tag,
        on_delete=RESTRICT,
    )

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'tag'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.tag}'


class RecipeShoppingCart(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.user}'


class RecipeFavorite(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
    )
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранные')
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.user}'
