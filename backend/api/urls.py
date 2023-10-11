from django.urls import include, path
from rest_framework import routers
from .views import (TagViewSet,
                    RecipeViewSet,
                    # FavoriteViewSet,
                    # ShoopingCartViewSet,
                    IngredientViewSet,)
                    # SubscribeViewSet)

router = routers.DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
#router.register(r'favorite', FavoriteViewSet)
#router.register(r'download_shooping_cart', ShoopingCartViewSet)
router.register(r'ingredients', IngredientViewSet)
#router.register(r'subscriptions', SubscribeViewSet)


urlpatterns = [
    path('', include(router.urls)),

]
