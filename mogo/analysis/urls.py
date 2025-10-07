from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnaliseViewSet  # Exemplo, ajuste conforme seu ViewSet

router = DefaultRouter()
router.register(r'analise', AnaliseViewSet, basename='analise')

urlpatterns = [
    path('', include(router.urls)),
]