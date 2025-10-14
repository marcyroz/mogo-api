from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RotaViewSet, LocalViewSet, HistoricoBuscaViewSet

router = DefaultRouter()
router.register(r'rota', RotaViewSet)
router.register(r'local', LocalViewSet)
router.register(r'historico', HistoricoBuscaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
