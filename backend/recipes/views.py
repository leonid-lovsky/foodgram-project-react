from common.pagination import PageLimitPagination
from common.permissions import IsAuthorOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Recipe
from .serializers import RecipeSerializer
from .filters import RecipeFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
