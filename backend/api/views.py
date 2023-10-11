from recipes.models import (Tag,
                            Recipe,
                            # FavoriteRecipe,
                            # ShoopingCart,
                            Ingredient)
#from users.models import (Subscribe)
from rest_framework import viewsets
from .serializers import (TagSerializer,
                          RecipeSerializer,
                        #   FavoriteRecipeSerializer,
                        #   ShoopingCartSerializer,
                          IngredientSerializer,
                        #   SubscribeSerializer,
                          RecipeReadSerializer
                          )
from rest_framework.permissions import SAFE_METHODS


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perfom_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeSerializer


# class FavoriteViewSet(viewsets.ModelViewSet):
#     queryset = FavoriteRecipe.objects.all()
#     serializer_class = FavoriteRecipeSerializer


# class ShoopingCartViewSet(viewsets.ModelViewSet):
#     queryset = ShoopingCart.objects.all()
#     serializer_class = ShoopingCartSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


# class SubscribeViewSet(viewsets.ModelViewSet):
#     queryset = Subscribe.objects.all()
#     serializer_class = SubscribeSerializer
