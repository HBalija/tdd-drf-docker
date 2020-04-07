from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Tag
from recipe.serializers import TagSerializer


class TagViewsSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin):
    """Manage tags in the database"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()  # for stupid router both this and get_queryset are required
    serializer_class = TagSerializer

    def get_queryset(self):
        """Return filtered queryset by user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create new tag"""
        serializer.save(user=self.request.user)
