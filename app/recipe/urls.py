from rest_framework.routers import DefaultRouter

from django.urls import include, path

from recipe.views import TagViewsSet

router = DefaultRouter()
router.register('tags', TagViewsSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
