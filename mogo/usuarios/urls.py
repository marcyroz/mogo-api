from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# Importe todos os ViewSets
from .views import UsuarioViewSet, PCDViewSet, TerceiroViewSet

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet, basename='usuario')
router.register(r'pcd', PCDViewSet, basename='pcd')
router.register(r'terceiro', TerceiroViewSet, basename='terceiro')

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
