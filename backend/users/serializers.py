from rest_framework import serializers
from users.models import User, Subscribe
from djoser.serializers import UserSerializer, UserCreateSerializer


class UserSerializer(UserSerializer):
    #is_subscribe = serializers.SerializerMethodField()

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


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = '__all__'

