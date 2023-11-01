from django_filters.rest_framework import FilterSet, filters
from recipes.models import Recipe, Tag, Ingredient


class RecipeFilter(FilterSet):
    """Фильтры для рецепта ."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        """Метакласс для RecipeFilter."""

        model = Recipe
        fields: tuple = ('author', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset


class IngredientFilter(FilterSet):
    """Фильтр для ингредиентов."""
    name = filters.CharFilter(lookup_expr='regex')

    class Meta:
        model = Ingredient
        fields: tuple = ('name',)
