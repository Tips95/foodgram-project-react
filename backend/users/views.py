from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from djoser.views import UserViewSet

from .serializers import UserSerializer, SubscribeCreateSerializer
from .models import User, Subscribe


class CustomUserViewSet(UserViewSet):
    """Вьюсет для работы с пользователями и подписками."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """Получение разрешений в зависимости от действия."""
        if self.action == "me":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        """Добавление или удаление подписки на другого пользователя."""
        user = request.user
        model = Subscribe
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscribeCreateSerializer(author, data=request.data,
                                                   context={'request': request})
            serializer.is_valid(raise_exception=True)
            model.objects.create(
                author=author, user=user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            subscribe = model.objects.filter(author=author, user=user)
            if subscribe.exists():
                subscribe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """Получение списка подписок текущего пользователя."""
        user = request.user
        queryset = User.objects.filter(
            following__user=user
        )
        page = self.paginate_queryset(queryset)
        serializer = SubscribeCreateSerializer(page,
                                               context={'request': request},
                                               many=True)
        return self.get_paginated_response(serializer.data)
