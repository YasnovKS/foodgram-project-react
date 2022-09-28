from multiprocessing import context
from rest_framework import serializers

from .fields import Base64ImageField
from food_app.models import (Tag, Recipe, RecipeTags,
                             RecipeIngredients, Ingredient)
from users.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

        fields = (
            'id',
            'title',
            'color',
            'slug'
        )
        lookup_field = 'id'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'


class GetIngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            read_only=True)
    name = serializers.SlugRelatedField(slug_field='name',
                                        source='ingredient',
                                        read_only=True)
    unit = serializers.SlugRelatedField(slug_field='unit',
                                        source='ingredient',
                                        read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'unit', 'amount')


class PostIngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient
                                            .objects.all()
                                            )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')


class GetRecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'title',
                  'description', 'image', 'cooking_time', 'pub_date')

    def get_ingredients(self, obj):
        queryset = obj.ingredients_list.all()
        return GetIngredientAmountSerializer(queryset, many=True).data


class PostRecipeSerializer(serializers.ModelSerializer):
    ingredients = PostIngredientsAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all()
                                              )
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=1000)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe

        fields = (
            'id',
            'tags',
            'ingredients',
            'author',
            'title',
            'image',
            'description',
            'cooking_time'
        )

    def create(self, validated_data):
        request = self.context['request']
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user,
                                       **validated_data)
        recipe.save()
        for ingredient in ingredients:
            RecipeIngredients.objects.create(recipe=recipe,
                                             ingredient=ingredient['id'],
                                             amount=ingredient['amount']
                                             )
        for tag in tags:
            RecipeTags.objects.create(recipe=recipe,
                                      tag=tag)
        return recipe

    def to_representation(self, instance):
        data = GetRecipeSerializer(instance,
                                   context={
                                       'request': self.context.get('request')
                                   }
                                   ).data
        return data
