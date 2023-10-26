from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Sum
from recipes.models import (Tag,
                            Recipe,
                            Ingredient,
                            FavoriteRecipe,
                            ShoppingCart,
                            IngredientAmount)
from rest_framework import viewsets
from .serializers import (TagSerializer,
                          RecipeSerializer,
                          IngredientSerializer,
                          RecipeReadSerializer,
                          RecipeShortSerializer,
                          )
from .permissions import IsAuthorOrReadOnly
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny,
                                        SAFE_METHODS)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = IsAuthorOrReadOnly,
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=('POST', 'DELETE')
    )
    def favorite(self, request, pk):
        user = request.user
        model = FavoriteRecipe
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = Recipe.objects.get(id=pk)
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            favorite = model.objects.filter(user=user, recipe__id=pk)
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @action(
        detail=True,
        methods=('POST', 'DELETE')
    )
    def shopping_cart(self, request, pk):
        user = request.user
        model = ShoppingCart
        if request.method == 'POST':
            if model.objects.filter(user=user, recipe__id=pk).exists():
                return Response(
                    {'errors': 'рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe = Recipe.objects.get(id=pk)
            model.objects.create(user=user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            shopcart = model.objects.filter(user=user, recipe__id=pk)
            if shopcart.exists():
                shopcart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def download_shopping_cart(self, request, *kwargs):
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
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
