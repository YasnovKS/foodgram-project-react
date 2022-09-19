from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView


class Index(ListView):
    queryset = Recipe.objects.all()
    context_object_name = 'recipes_list'
    template_name = 'recipes/index.html'
