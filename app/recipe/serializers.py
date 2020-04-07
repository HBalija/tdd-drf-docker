from rest_framework import serializers

from recipe.models import Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objec"t"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
