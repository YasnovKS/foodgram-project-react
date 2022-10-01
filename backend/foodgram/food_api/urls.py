from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import RecipeViewSet, SubscribeView, TagsViewSet, FavoriteView

app_name = 'food_api'

router = SimpleRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls), name='food_api'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view(),
         name='favorite'),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view(),
         name='subscribe'),
]
