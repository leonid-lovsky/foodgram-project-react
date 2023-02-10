from common.permissions import IsAuthorOrReadOnly
from django.shortcuts import render
from rest_framework import permissions, viewsets

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
