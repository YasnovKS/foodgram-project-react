from .models import Ingredient, Recipe, Tag, RecipeIngredients
from django.contrib import admin


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description',
                    'cooking_time', 'pub_date')
    list_filter = ('author', 'title')
    ordering = ['-pub_date']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    list_filter = ('name',)
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'slug')
    list_filter = ('title', 'color')


admin.site.register(RecipeIngredients)
