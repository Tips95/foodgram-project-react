from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from colorfield.fields import ColorField
from users.models import User


class Ingredient(models.Model):
    """Модель ингредиентов."""

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering: tuple = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    color = ColorField(
        verbose_name='Цвет',
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        unique=True,
    )

    class Meta:
        ordering: tuple = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор публикации',
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название блюда',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Фото блюда',
        upload_to='recipes/'
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        max_length=255
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='ingredients',
        verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='тег',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления в минутах',
        validators=(
            MinValueValidator(1, 'Минимум 1 минута'),
            MaxValueValidator(180, 'Максимум 3 часа'),
        )
    )

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    """Модель количества ингредиентов в рецептах."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_list',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        'Количество',
        default=1,
        validators=(
            MinValueValidator(1, 'Минимум 1 ингредиент'),
        )
    )

    class Meta:
        ordering: tuple = ('id',)
        verbose_name: str = 'Количество ингредиента'
        verbose_name_plural: str = 'Количество ингредиентов'

    def __str__(self) -> str:
        return (f'В рецепте {self.recipe.name} '
                f'{self.count}{self.ingredient.measurement_unit} '
                f'{self.ingredient.name}')


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='корзина',
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints: list = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe}'


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name: str = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints: list = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite',)
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.recipe}'
