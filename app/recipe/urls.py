from rest_framework.routers import DefaultRouter

from django.urls import include, path

from recipe.views import IngredientViewsSet, RecipeViewSet, TagViewsSet

router = DefaultRouter()
router.register('tags', TagViewsSet)
router.register('ingredients', IngredientViewsSet)
router.register('recipes', RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
