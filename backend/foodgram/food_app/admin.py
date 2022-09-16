from .models import Recipe, Tag
from django.contrib import admin


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description',
                    'tag', 'cooking_time',
                    'pub_date')
    list_filter = ('author', 'title')
    ordering = ['-pub_date']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'color', 'slug')
    list_filter = ('title', 'color')
