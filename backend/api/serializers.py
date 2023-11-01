from rest_framework import serializers
from recipes.models import (Tag,
                            Recipe,
                            FavoriteRecipe,
                            ShoppingCart,
                            Ingredient,
                            IngredientAmount
                            )
from users.models import (Subscribe)
from users.serializers import UserSerializer
import base64
from django.core.files.base import ContentFile


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для кодирования изображения в ba64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientAmount."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe."""

    image = Base64ImageField(required=True, allow_null=False)
    ingredients = IngredientAmountSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'cooking_time', 'tags', 'author',
                  'ingredients', 'image',)

    def validate(self, data):
        """Проверка данных при создании или обновлении рецепта."""
        ingredients_data = data.get('ingredients')
        tags_data = data.get('tags')
        valid_tags = []
        valid_ingredients = []
        if not tags_data:
            raise serializers.ValidationError('Должен быть хотя бы 1 тег')
        for tag in tags_data:
            if tag in valid_tags:
                raise serializers.ValidationError('Нельзя добавить один тег 2 раза')
            valid_tags.append(tag)

        if not ingredients_data:
            raise serializers.ValidationError('должен быть хотя бы 1 ингредиент')
        for ingredient in ingredients_data:
            try:
                ing_id = Ingredient.objects.get(id=ingredient['ingredient']['id'])
                print(ing_id)
            except Exception:
                raise serializers.ValidationError('Ингредиент не существует')
            if ingredient in valid_ingredients:
                raise serializers.ValidationError('Нельзя добавить один ингредиент 2 раза')
            valid_ingredients.append(ingredient)
        return data

    def ingredient_amount(self, ingregients, recipe):
        """Создание связей между рецептом и ингредиентами."""
        for ingredient in ingregients:
            id = ingredient['ingredient']['id']
            amount = ingredient['amount']
            recipe.ingredients_list.create(
                amount=amount,
                recipe_id=recipe.id,
                ingredient_id=Ingredient.objects.get(id=id).id
            )

    def create(self, validated_data):
        """Создание нового рецепта."""
        ingredients = validated_data.pop('ingredients')
        tag = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tag)
        self.ingredient_amount(recipe=recipe, ingregients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        """Обновление существующего рецепта."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(tags)
        self.ingredient_amount(recipe=instance, ingregients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Преобразование модели Recipe в представление."""
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance, context=context).data


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Recipe."""
    image = serializers.SerializerMethodField(required=False, allow_null=True)
    ingredients = IngredientAmountSerializer(many=True,
                                             source='ingredients_list')
    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'text', 'cooking_time', 'tags', 'author',
                  'ingredients', 'image', 'is_favorited', 'is_in_shopping_cart',)

    def get_is_favorited(self, obj):
        """Проверка, добавлен ли рецепт в избранное."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite_recipe.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверка, добавлен ли рецепт в список покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()

    def get_image(self, obj) -> image:
        """Получение URL изображения рецепта."""
        if obj.image:
            return obj.image.url


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели FavoriteRecipe."""

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ShoppingCart."""

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscribe."""

    class Meta:
        model = Subscribe
        fields = '__all__'


class RecipeShortSerializer(serializers.ModelSerializer):
    """Сериализатор для краткого представления модели Recipe."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
