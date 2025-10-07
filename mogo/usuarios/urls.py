from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, PCDViewSet, TerceiroViewSet  # Importe todos os ViewSets

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')
router.register(r'pcd', PCDViewSet, basename='pcd')
router.register(r'terceiro', TerceiroViewSet, basename='terceiro')

urlpatterns = [
    path('', include(router.urls)),
]