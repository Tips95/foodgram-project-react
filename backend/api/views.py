from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny,
                                        SAFE_METHODS,
                                        IsAuthenticated)
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    FavoriteRecipe,
    ShoppingCart,
    IngredientAmount,
    User,
)
from .serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeShortSerializer,
)
from .permissions import IsAuthorOrReadOnly
from .filters import IngredientFilter, RecipeFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки запросов на получение тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes: tuple = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с рецептами."""

    queryset = Recipe.objects.all()
    permission_classes: tuple = (IsAuthorOrReadOnly,)
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """Создание нового рецепта."""
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Получение класса сериализатора в зависимости от метода запроса."""
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk) -> Response:
        """Добавление или удаление рецепта в избранное."""
        user: User = request.user
        model = FavoriteRecipe
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            recipe: Recipe = get_object_or_404(Recipe, id=pk)
            favorite = model.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk) -> Response:
        """Добавление или удаление рецепта в список покупок."""
        user: User = request.user
        model = ShoppingCart
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                recipe = Recipe.objects.get(id=pk)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            recipe: Recipe = get_object_or_404(Recipe, id=pk)
            shopcart = model.objects.filter(user=user, recipe=recipe)
            if shopcart.exists():
                shopcart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, *kwargs):
        """Скачивание списка покупок в формате текстового файла."""
        user = request.user
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shop_list = ('Ваш список покупок \n')
        for ingredient in ingredients:
            shop_list += '\n'.join([
                f" {ingredient['ingredient__name']} "
                f" ({ingredient['ingredient__measurement_unit']}) "
                f" - {ingredient['amount']}"
            ])

        file = 'shop_list.txt'
        response = HttpResponse(shop_list, content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename={file}'
        )
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для обработки запросов на получение ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends: tuple = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
