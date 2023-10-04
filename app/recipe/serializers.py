from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


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


class RecipeSerializer(serializers.ModelSerializer):
    """Model definition for RecipeSerializer."""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        """Meta definition for IngredientSerializer."""
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags',
                  'time_minutes', 'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize the recipe details"""
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
