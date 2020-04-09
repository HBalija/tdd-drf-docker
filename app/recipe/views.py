from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipe.models import Ingredient, Recipe, Tag
from recipe.serializers import (
    IngredientSerializer, RecipeDetailSerializer, RecipeImageSerializer, RecipeSerializer,
    TagSerializer
)


class BaseRecipeAttrViewSet(viewsets.GenericViewSet, ListModelMixin, CreateModelMixin):
    """ Base viewset for user owned recipe attributes """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Return filtered queryset by user """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewsSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewsSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):

    serializer_class = RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Recipe.objects.all()

    def _params_to_ints(self, qs):
        """ Convert a string of IDs to a list of integers. """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset.filter(user=self.request.user)
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ing_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ing_ids)

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        if self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # define a custom POST action for this viewset
    # for a single object (detail=True)
    # url = detail url + url_path (recipes/1/upload-image)
    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a recipe using recipe pk """

        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
