# Generated by Django 4.1.1 on 2022-10-06 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='ingredients', through='food_app.RecipeIngredients', to='food_app.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ingredients_list', to='food_app.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipeingredients',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_list', to='food_app.recipe', verbose_name='Рецепт'),
        ),
    ]