from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

COLOR_VALIDATOR = RegexValidator(
    r'^#[a-fA-F0-9]{6}$',
    _('Используйте RGB-формат для указания цвета (#FFFFFF)'),
)


class Tag(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        _('Цвет'),
        max_length=7,
        validators=[COLOR_VALIDATOR],
        unique=True,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        _('Название'),
        max_length=200,
        blank=False,
    )
    measurement_unit = models.CharField(
        _('Единицы измерения'),
        max_length=200,
        blank=False,
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name=_('Автор'),
    )
    name = models.CharField(
        _('Название'),
        max_length=200,
    )
    image = models.ImageField(
        _('Картинка'),
        upload_to='recipes/images',
    )
    text = models.TextField(
        _('Описание'),
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name=_('Ингредиенты'),
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name=_('Теги'),
    )
    cooking_time = models.IntegerField(
        _('Время приготовления'),
        validators=[
            MinValueValidator(1),
        ],
    )
    pub_date = models.DateTimeField(
        _('Дата публикации'),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = _('Рецепт')
        verbose_name_plural = _('Рецепты')
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.RESTRICT,
    )

    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.tag}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.RESTRICT,
    )
    amount = models.IntegerField(
        _('Количество'),
        validators=[
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = _('Ингредиент')
        verbose_name_plural = _('Ингредиенты')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class RecipeInShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Корзина')
        verbose_name_plural = _('Корзины')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.user}'


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _('Избранное')
        verbose_name_plural = _('Избранные')
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
        ]

    def __str__(self):
        return f'{self.user}'


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscribing',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='subscribers',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='%(app_label)s_%(class)s_unique_relationships'
            ),
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_prevent_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        ]
