from django.db import models
from users.models import User


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
        return self.name


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
                                         through='RecipeIngredients')
    tag = models.ForeignKey(Tag,
                            on_delete=models.SET_NULL,
                            null=True,
                            verbose_name='Тег')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата создания')

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredients(models.Model):
    '''Helping model for many-to-many relationship.'''
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.DO_NOTHING,
                                   verbose_name='Ингредиент')
    count = models.IntegerField(verbose_name='Количество')
