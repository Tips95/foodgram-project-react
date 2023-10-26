from django.shortcuts import get_object_or_404
from rest_framework import status
from djoser.views import UserViewSet
from requests import Response
from rest_framework.decorators import action
from .serializers import UserSerializer
from .models import User, Subscribe


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    #permission_classes = 
    serializer_class = UserSerializer


