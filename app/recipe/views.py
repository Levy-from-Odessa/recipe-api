from recipe.serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer
from core.models import Tag, Ingredient, Recipe

from rest_framework import viewsets, mixins, authentication, permissions


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new attr"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-title')

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class
