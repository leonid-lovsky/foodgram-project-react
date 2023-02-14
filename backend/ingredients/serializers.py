from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, SerializerMethodField
)

from .models import Ingredient


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'measurement_unit',
        ]
