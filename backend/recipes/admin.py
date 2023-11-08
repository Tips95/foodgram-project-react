from django.contrib import admin

from .models import (Ingredient, Tag, Recipe, IngredientAmount,
                     ShoppingCart, FavoriteRecipe)


class IngredientAdmin(admin.ModelAdmin):
    """Админка для модели Ingredient."""

    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')


class TagAdmin(admin.ModelAdmin):
    """Админка для модели Tag."""

    list_display = ('name', 'color', 'slug')


class RecipeAdmin(admin.ModelAdmin):
    """Админка для модели Recipe."""

    list_display = ('name', 'author', 'cooking_time', 'get_favorite_count')
    readonly_fields: tuple = ('get_favorites_count',)
    list_filter = ('author', 'tags')
    search_fields = ('name', 'author', 'tags')

    def get_favorite_count(self, obj):
        return obj.favorite_recipe.count()
    get_favorite_count.short_description = 'Избранное'


class IngredientAmountAdmin(admin.ModelAdmin):
    """Админка для модели IngredientAmount."""

    list_display = ('recipe', 'ingredient', 'amount')


class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для модели ShoppingCart."""

    list_display = ('user', 'recipe')


class FavoriteRecipeAdmin(admin.ModelAdmin):
    """Админка для модели FavoriteRecipe."""

    list_display = ('user', 'recipe')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
