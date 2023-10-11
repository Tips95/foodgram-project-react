from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
    )
    slug = models.SlugField(
        verbose_name='Слаг тега',
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
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
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        default=1,
        validators=(
            MinValueValidator(1, 'Минимум 1 минута'),
            MaxValueValidator(180, 'Максимум 3 часа'),
        )
    )

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
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
        ordering = ('id',)
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_count'
            )
        ]

    def __str__(self):
        return f'В рецепте {self.recipe.name} {self.count}{self.ingredient.measurement_unit} {self.ingredient.name}'


class ShoopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='shooping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='корзина',
        related_name='shooping_cart'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe}'


class FavoriteRecipe(models.Model):
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
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite',)
        ]

    def __str__(self):
        return f'{self.user} подписался на {self.recipe}'
