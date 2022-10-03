from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (RecipeViewSet, SubscribeView, TagsViewSet, FavoriteView,
                    SubscriptionsView, IngredientsViewSet, ShoppingCartView)

app_name = 'food_api'

router = SimpleRouter()

router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', ShoppingCartView.as_view(),
         name='dowload_cart'),
    path('', include(router.urls), name='food_api'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view(),
         name='favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view(),
         name='cart'),
    path('users/subscriptions/', SubscriptionsView.as_view(),
         name='subscriptions'),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view(),
         name='subscribe'),
]
