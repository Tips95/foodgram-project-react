from django.contrib import admin

from .models import User, Subscribe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование модели User."""

    list_display: list = ['email', 'username', 'first_name', 'last_name']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Администрирование модели Subscribe."""

    list_display: list = ['user', 'author']
