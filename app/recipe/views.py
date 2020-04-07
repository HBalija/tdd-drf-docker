from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.models import Ingredient, Tag
from recipe.serializers import IngredientSerializer, TagSerializer


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin):
    """Base viewset for user owned recipe attributes"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return filtered queryset by user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class TagViewsSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    queryset = Tag.objects.all()  # for stupid router both this and get_queryset are required
    serializer_class = TagSerializer


class IngredientViewsSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database"""

    queryset = Ingredient.objects.all()  # for stupid router both this and get_queryset are required
    serializer_class = IngredientSerializer
