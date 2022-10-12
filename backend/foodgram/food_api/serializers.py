from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import Base64ImageField
from food_app.models import (FavoriteRecipe, Ingredient, Recipe,
                             RecipeIngredients, RecipeTags, ShoppingCart, Tag)
from users.models import Subscribe

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
            'name',
            'color',
            'slug'
        )
        lookup_field = 'id'


class GetTagsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='tag',
                                            read_only=True)
    name = serializers.SlugRelatedField(source='tag',
                                        slug_field='name',
                                        read_only=True)
    color = serializers.SlugRelatedField(source='tag',
                                         slug_field='color',
                                         read_only=True)
    slug = serializers.SlugRelatedField(source='tag',
                                        slug_field='slug',
                                        read_only=True)

    class Meta:
        model = RecipeTags
        fields = ('id', 'name', 'color', 'slug')


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
    measurement_unit = (serializers.
                        SlugRelatedField(slug_field='measurement_unit',
                                         source='ingredient',
                                         read_only=True))

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount')


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
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'author', 'name',
                  'text', 'image', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_ingredients(self, obj):
        queryset = obj.recipes_list.all()
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

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and ShoppingCart.objects.filter(recipe=obj,
                                                user=request.user
                                                ).exists()
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
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')
        checking_ingredients = list()

        for ingredient in ingredients:
            if not ingredient['id']:
                raise serializers.ValidationError('Не указаны ингредиенты'
                                                  ' для рецепта.')
            if not ingredient['amount'] or int(ingredient['amount']) < 1:
                name = Ingredient.objects.get(pk=ingredient['id']).name
                raise serializers.ValidationError('Не указано количество'
                                                  f' для {name}')
            if ingredient['id'] in checking_ingredients:
                raise serializers.ValidationError('Ингредиенты не могут'
                                                  ' повторяться.')
            checking_ingredients.append(ingredient['id'])

        if not tags:
            raise serializers.ValidationError('Не указаны теги'
                                              ' для рецепта.')
        if (not self.initial_data.get('cooking_time')
                or int(self.initial_data.get('cooking_time')) < 1):
            raise serializers.ValidationError('Не указано время'
                                              ' приготовления блюда.')
        return data

    def create_related_objects(self, recipe, ingredients, tags):
        ingredients_list = list()
        tags_list = list()
        for ingredient in ingredients:
            ingr_object = RecipeIngredients(recipe=recipe,
                                            ingredient=ingredient['id'],
                                            amount=ingredient['amount']
                                            )
            ingredients_list.append(ingr_object)
        for tag in tags:
            tag_object = RecipeTags(recipe=recipe, tag=tag)
            tags_list.append(tag_object)

        RecipeIngredients.objects.bulk_create(ingredients_list)
        RecipeTags.objects.bulk_create(tags_list)

    def create(self, validated_data):
        request = self.context['request']
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user,
                                       **validated_data)
        recipe.save()
        self.create_related_objects(recipe, ingredients, tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        Recipe.objects.filter(pk=instance.id).update(**validated_data)
        recipe = Recipe.objects.get(id=instance.id)
        RecipeIngredients.objects.filter(recipe=recipe).delete()
        RecipeTags.objects.filter(recipe=recipe).delete()
        self.create_related_objects(recipe, ingredients, tags)
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
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes.count',
                                             read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit_value = request.get('recipes_limit')
        recipes = obj.recipes.all()[:limit_value]
        request = self.context.get('request')
        return ShortRecipeSerializer(
            recipes, many=True,
            context={'request': request}
        ).data
