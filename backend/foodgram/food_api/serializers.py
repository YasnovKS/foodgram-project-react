from django.contrib.auth import get_user_model
from food_app.models import (FavoriteRecipe, Ingredient, Recipe,
                             RecipeIngredients, RecipeTags, Tag)
from rest_framework import serializers
from users.models import Subscribe

from .fields import Base64ImageField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        extra_kwargs = {"password": {'write_only': True}}

    def get_is_subscribed(self, obj):
        author = obj
        request = self.context.get('request')
        try:
            follower = request.user
            return Subscribe.objects.filter(follower=follower,
                                            author=author).exists()
        except TypeError:
            return False


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


class GetTagsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='tag',
                                            read_only=True)
    title = serializers.SlugRelatedField(source='tag',
                                         slug_field='title',
                                         read_only=True)
    color = serializers.SlugRelatedField(source='tag',
                                         slug_field='color',
                                         read_only=True)
    slug = serializers.SlugRelatedField(source='tag',
                                        slug_field='slug',
                                        read_only=True)

    class Meta:
        model = RecipeTags
        fields = ('id', 'title', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
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
    tags = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'title',
                  'description', 'image', 'cooking_time', 'is_favorited')

    def get_ingredients(self, obj):
        queryset = obj.ingredients_list.all()
        return GetIngredientAmountSerializer(queryset, many=True).data

    def get_tags(self, obj):
        queryset = obj.tags_list.all()
        return GetTagsSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and FavoriteRecipe.objects.filter(recipe=obj,
                                                  user=request.user).exists()
                )


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

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.id).update(**validated_data)
        recipe = Recipe.objects.get(id=instance.id)
        RecipeIngredients.objects.filter(recipe=recipe).delete()
        RecipeTags.objects.filter(recipe=recipe).delete()
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


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'image', 'cooking_time')
        read_only_fields = ('title', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
