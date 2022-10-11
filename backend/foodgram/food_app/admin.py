from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (FavoriteRecipe, Ingredient, Recipe, RecipeIngredients,
                     RecipeTags, ShoppingCart, Tag)

User = get_user_model()


class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    min_num = 1


class TagsInline(admin.TabularInline):
    model = RecipeTags
    min_num = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('first_name', 'email')


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'text',
                    'cooking_time', 'pub_date', 'display_tags',
                    'display_ingredients', 'in_favorites')
    list_filter = ('author', 'name', 'tags', 'ingredients')
    search_fields = ('author__first_name', 'author__email', 'name',
                     'tags__name', 'ingredients__name')
    ordering = ['-pub_date']
    inlines = (RecipeIngredientsInline, TagsInline)

    def display_ingredients(self, obj):
        return list([ingredient.name for ingredient in obj.ingredients.all()])
    display_ingredients.short_description = 'Ингредиенты'

    def display_tags(self, obj):
        return list([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Теги'

    def in_favorites(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()
    in_favorites.short_description = 'В избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filter = ('name', 'color')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user__username', 'user__email', 'recipe__name')


admin.site.register(RecipeIngredients)
admin.site.register(RecipeTags)
