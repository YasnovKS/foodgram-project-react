from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):
    '''Model for creating ingredients.'''
    name = models.CharField(max_length=100,
                            verbose_name='Название')
    unit = models.CharField(max_length=20,
                            verbose_name='Ед. изм.')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return (self.name)


class Tag(models.Model):
    '''This model defines tags for taggins recipes.'''
    title = models.CharField(max_length=50,
                             verbose_name='Название')
    color = models.CharField(max_length=50,
                             verbose_name='Цвет тега')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг тега',
                            auto_created=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    '''Model for recipes.'''
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='recipes')
    title = models.CharField(max_length=300,
                             verbose_name='Название')
    image = models.ImageField(verbose_name='Картинка')
    description = models.TextField(max_length=1000,
                                   verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(Ingredient,
                                         related_name='recipes',
                                         through='RecipeIngredients',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes',
                                  verbose_name='Тег')
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время'
                                                    'приготовления',
                                                    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата создания')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredients(models.Model):
    '''
    Helping model to many-to-many relationship
    for recipes and ingredients.
    '''
    recipe = models.ForeignKey(Recipe,
                               related_name='ingredients_list',
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipes_list',
                                   on_delete=models.DO_NOTHING,
                                   verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'ingredient'),
                                    name='unique_recipe_ingredient_set')
        ]


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='tags_list')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='recipes_list')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('recipe', 'tag'),
                                    name='unique_recipe_tag_set')
        ]


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_recipes',
                             verbose_name='Избранное')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_users')

    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_list')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='in_users_cart')

    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_cart')
        ]
