from django_filters import rest_framework as filter

from food_app.models import Ingredient, Recipe


class IngredientFilter(filter.FilterSet):
    name = filter.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(filter.FilterSet):
    author = filter.CharFilter(field_name='author__username')
    tags = filter.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
