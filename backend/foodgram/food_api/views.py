from food_app.models import Recipe
from .mixins import ListDetailViewSet
from food_app.models import Tag, Recipe
from .serializers import TagSerializer, RecipeSerializer
from rest_framework import (filters, pagination, permissions,
                            viewsets)
from foodgram.settings import INDEX_PAGE_SIZE


class TagsViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$title',)
    pagination_class = pagination.PageNumberPagination
    permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = pagination.PageNumberPagination
    pagination_class.page_size = INDEX_PAGE_SIZE
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action != 'GET':
            return RecipeSerializer
