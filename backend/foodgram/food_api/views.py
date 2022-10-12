from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import (filters, generics, pagination, permissions,
                            serializers, status, views, viewsets)
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .mixins import GetObjectsViewSet, ListDetailViewSet
from .permissions import EditPermission
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          PostRecipeSerializer, ShortRecipeSerializer,
                          SubscribeSerializer, TagSerializer)
from .services import generate_shopping_list
from food_app.models import (FavoriteRecipe, Ingredient, Recipe,
                             RecipeIngredients, ShoppingCart, Tag)
from users.models import Subscribe, User


class SubscribeView(views.APIView):
    '''
    This view helps users to follow and unfollow
    recipes authors.
    '''
    permission_classes = (permissions.IsAuthenticated,
                          EditPermission)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=user_id)
        if author == request.user:
            raise serializers.ValidationError('Нельзя подписаться'
                                              ' на самого себя.')
        serializer = SubscribeSerializer(author,
                                         context={'request': request}
                                         )
        subscribe, created = (Subscribe.objects.
                              get_or_create(author=author,
                                            follower=request.user)
                              )
        if not created:
            raise serializers.ValidationError('Вы уже подписаны'
                                              ' на данного автора.')
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=user_id)
        instance = Subscribe.objects.filter(author=author,
                                            follower=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = SubscribeSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        return User.objects.filter(followed__follower=self.request.user)


class TagsViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$name',)
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          EditPermission)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action not in permissions.SAFE_METHODS:
            return PostRecipeSerializer
        return GetRecipeSerializer


class FavoriteView(views.APIView):
    '''
    This view helps users to manage recipes
    in "favorite"
    '''
    queryset = Recipe.objects.all()
    serializer_class = ShortRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,
                          EditPermission)

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = ShortRecipeSerializer(recipe)
        favorite, created = (FavoriteRecipe.objects.
                             get_or_create(recipe=recipe,
                                           user=request.user))
        if not created:
            raise serializers.ValidationError('Рецепт уже добавлен'
                                              ' в избранное.')
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        instance = FavoriteRecipe.objects.filter(recipe=recipe,
                                                 user=request.user)
        if not instance:
            raise serializers.ValidationError('Рецепт отсутствует'
                                              ' в избранном.')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(GetObjectsViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class ShoppingCartView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,
                          EditPermission)

    def get(self, request):
        with transaction.atomic():
            queryset = (RecipeIngredients.objects.
                        filter(recipe__in_users_cart__user=request.user))
            shopping_list = generate_shopping_list(queryset)
            ShoppingCart.objects.filter(user=request.user).delete()

            response = HttpResponse(shopping_list, 'Content-type: text/plain')
            response['Content-Disposition'] = ('attachment; filename='
                                               '"Shopping.txt"')
            return response

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer = ShortRecipeSerializer(recipe,
                                           context={'request': request})
        cart, created = ShoppingCart.objects.get_or_create(recipe=recipe,
                                                           user=request.user)
        if not created:
            raise serializers.ValidationError('Рецепт уже в списке покупок.')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        instance = ShoppingCart.objects.filter(recipe=recipe,
                                               user=request.user)
        if not instance:
            raise serializers.ValidationError('Рецепт отсутствует в'
                                              ' списке покупок.')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
