from rest_framework import serializers
from core.models import Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Model definition for TagSerializer."""

    class Meta:
        """Meta definition for TagSerializer."""
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Model definition for IngredientSerializer."""

    class Meta:
        """Meta definition for IngredientSerializer."""
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)
