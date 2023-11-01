from django.contrib import admin
from .models import User, Subscribe
from recipes.models import Ingredient


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Администрирование модели User."""

    list_display = ['email', 'username', 'first_name', 'last_name']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    """Администрирование модели Subscribe."""

    list_display = ['user', 'author']

@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    """Администрирование модели Ingredient."""

    list_display = ["name", "measurement_unit"]
    search_fields = ["name"]
    list_filter = ["name"]
