from rest_framework.routers import DefaultRouter

from django.urls import include, path

from recipe.views import IngredientViewsSet, TagViewsSet

router = DefaultRouter()
router.register('tags', TagViewsSet)
router.register('ingredients', IngredientViewsSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
