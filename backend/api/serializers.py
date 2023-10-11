from rest_framework import serializers
from recipes.models import (Tag,
                            Recipe,
                            FavoriteRecipe,
                            ShoopingCart,
                            Ingredient,
                            IngredientAmount
                            )
from users.models import (Subscribe)
from users.serializers import UserSerializer
import base64
from django.core.files.base import ContentFile


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientAmountSerializer(many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def ingredient_amount(self, ingregients, recipe):
        for ingredient in ingregients:
            id = ingredient['id']
            amount = ingredient['amount']
            recipe.ingredients_list.create(
                amount=amount,
                recipe_id=recipe.id,
                ingredient_id=Ingredient.objects.get(id=id).id
            )

    def create(self, validated_data):
        print(validated_data)
        ingredients = validated_data.pop('ingredients')
        print(ingredients)
        tag = validated_data.pop('tags')
        print(tag)
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tag)
        self.ingredient_amount(recipe=recipe, ingregients=ingredients)
        return recipe

    #def update(self, instance, validated_data):
    #

class RecipeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = '__all__'


class ShoopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoopingCart
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'
