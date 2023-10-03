from recipe.serializers import TagSerializer
from core.models import Tag
from django.http import HttpResponse

from rest_framework import viewsets, mixins, authentication, permissions


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        user = self.request.user
        # if user.is_anonymous:
        #     return HttpResponse('401 Unauthorized', status=401)
        return self.queryset.filter(user=user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)
