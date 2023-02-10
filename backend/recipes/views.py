from common.pagination import PageLimitPagination
from common.permissions import IsAuthorOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    pagination_class = PageLimitPagination
    pagination_class.page_size = 6

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
