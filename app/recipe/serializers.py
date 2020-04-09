from rest_framework import serializers

from recipe.models import Ingredient, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')


class RecipeSerializer(serializers.ModelSerializer):

    ingredients = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link')


class RecipeDetailSerializer(RecipeSerializer):

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to recipes """

    class Meta:
        model = Recipe
        fields = ('id', 'image')
