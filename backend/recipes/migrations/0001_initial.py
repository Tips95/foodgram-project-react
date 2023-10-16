# Generated by Django 3.2 on 2023-09-30 15:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=50, verbose_name='Единица измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('color', models.CharField(choices=[('#FF5733', 'Red'), ('#33FF57', 'Green'), ('#5733FF', 'Blue'), ('#FF33C6', 'Pink'), ('#33C6FF', 'Cyan'), ('#FFFF33', 'Yellow')], max_length=7, verbose_name='Цвет')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг тега')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('image', models.ImageField(upload_to='recipe_images/', verbose_name='Фото блюда')),
                ('text', models.TextField(max_length=255, verbose_name='Описание блюда')),
                ('cooking_time', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Минимум 1 минута'), django.core.validators.MaxValueValidator(180, 'Максимум 3 часа')], verbose_name='Время приготовления в минутах')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор публикации')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, 'Минимум 1 ингредиент'), django.core.validators.MaxValueValidator(30, 'Максимум 30 ингредиентов')], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='count', to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe')),
            ],
            options={
                'verbose_name': 'Количество ингредиента',
                'verbose_name_plural': 'Количество ингредиентов',
                'ordering': ('id',),
            },
        ),
        migrations.AddConstraint(
            model_name='ingredientcount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_count'),
        ),
    ]