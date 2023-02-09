from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from serializers import RecipeSerializer

from models import Recipe
from common.permissions import IsOwnerOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
