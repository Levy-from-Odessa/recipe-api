from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Model definition for TagSerializer."""

    class Meta:
        """Meta definition for TagSerializer."""
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
