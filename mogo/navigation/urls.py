from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RotaViewSet, LocalViewSet, HistoricoDeBuscaViewSet  

router = DefaultRouter()
router.register(r'rota', RotaViewSet, basename='rota')
router.register(r'local', LocalViewSet, basename='local')
router.register(r'historico_de_busca', HistoricoDeBuscaViewSet, basename='historico_de_busca')

urlpatterns = [
    path('', include(router.urls)),
]