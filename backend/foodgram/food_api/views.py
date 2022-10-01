from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from food_app.models import FavoriteRecipe, Recipe, Tag
from users.models import Subscribe, User
from foodgram.settings import INDEX_PAGE_SIZE
from rest_framework import (filters, pagination, permissions, status, views,
                            viewsets)
from rest_framework.response import Response

from .mixins import ListDetailViewSet
from .permissions import EditPermission
from .serializers import (FavoriteRecipeSerializer, GetRecipeSerializer,
                          PostRecipeSerializer, TagSerializer,
                          SubscribeSerializer)


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
        serializer = SubscribeSerializer(author,
                                         context={'request': request}
                                         )
        subscribe, created = (Subscribe.objects.
                              get_or_create(author=author,
                                            follower=request.user)
                              )
        if created:
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response('Вы уже подписаны на автора.',
                            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=user_id)
        instance = Subscribe.objects.filter(author=author,
                                            follower=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagsViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$title',)
    pagination_class = pagination.PageNumberPagination
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = INDEX_PAGE_SIZE
    permission_classes = (EditPermission,
                          permissions.IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        if self.action not in ['GET', 'HEAD', 'OPTIONS']:
            return PostRecipeSerializer
        return GetRecipeSerializer


class FavoriteView(views.APIView):
    '''
    This view helps users to manage recipes
    in "favorite"
    '''
    queryset = Recipe.objects.all()
    serializer_class = FavoriteRecipeSerializer
    permission_classes = (permissions.IsAuthenticated,
                          EditPermission)

    def post(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer = FavoriteRecipeSerializer(recipe)
        favorite, created = (FavoriteRecipe.objects.
                             get_or_create(recipe=recipe,
                                           user=request.user))
        if created:
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response('Рецепт уже добавлен в избранное.',
                            status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        instance = FavoriteRecipe.objects.filter(recipe=recipe,
                                                 user=request.user)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
