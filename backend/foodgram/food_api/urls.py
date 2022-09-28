from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, TagsViewSet

app_name = 'food_api'

router = SimpleRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls), name='food_api'),
]
