from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvaliacaoViewSet, FavoritoViewSet

router = DefaultRouter()
router.register(r'avaliacao', AvaliacaoViewSet, basename='avaliacao')
router.register(r'favorito', FavoritoViewSet, basename='favorito')

urlpatterns = [
    path('', include(router.urls)),
]