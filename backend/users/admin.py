from django.contrib import admin
from .models import User, Subscribe
from recipes.models import Ingredient, Tag


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ['user', 'author']

@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ["name", "measurement_unit"]
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    pass