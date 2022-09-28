from rest_framework import serializers

from food_app.models import (Tag, Recipe,
                             RecipeIngredients, Ingredient)


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag

        fields = (
            'id',
            'title',
            'color',
            'slug'
        )


class IngrediensSerializer(serializers.ModelSerializer):

    class Meta:
        pass


class IngredientsAmountSerializer(serializers.ModelSerializer):
    ingredient = serializers.PrimaryKeyRelatedField(source='Ingredient',
                                                    read_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('ingredient', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientsAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              source='Tag',
                                              read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True,
                                          default=serializers.
                                          CurrentUserDefault()
                                          )

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
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.get_or_create(**validated_data)

        for ingredient in ingredients:
            obj = Ingredient.objects.get(pk=ingredient['id'])
            amount = ingredient['amount']
            RecipeIngredients.objects.get_or_create(recipe=recipe,
                                                    ingredient=obj,
                                                    amount=amount
                                                    )
        return recipe
