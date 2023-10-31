from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from users.models import User, Subscribe
from djoser.serializers import (UserSerializer,
                                UserCreateSerializer)
from api.serializers import RecipeShortSerializer


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request').user
        if request.is_anonymous:
            return False
        return Subscribe.objects.filter(author=obj, user=request).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SubscribeCreateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = SerializerMethodField(read_only=True)

    class Meta:
        model = Subscribe
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            )

    def get_is_subscribed(self, obj):
        print(obj)
        request = self.context.get('request').user
        if request.is_anonymous:
            return False
        return Subscribe.objects.filter(author=obj, user=request).exists()

    def get_recipes(self, obj):
        queryset = obj.recipes.all()
        return RecipeShortSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if user == author:
            raise serializers.ValidationError('Нельзя подписаться на самого себя')
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError('Нельзя повторно подписаться на автора')
        return data
