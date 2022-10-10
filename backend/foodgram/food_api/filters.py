from django_filters import rest_framework as filter
from rest_framework.filters import SearchFilter

from food_app.models import Recipe


class IngredientFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filter.FilterSet):
    author = filter.CharFilter(field_name='author__username')
    tags = filter.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
