# navigation/views.py
from rest_framework import viewsets
from .models import Rota, Local, HistoricoBusca
from .serializers import RotaSerializer, LocalSerializer, HistoricoBuscaSerializer

class RotaViewSet(viewsets.ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer

class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

class HistoricoBuscaViewSet(viewsets.ModelViewSet):
    queryset = HistoricoBusca.objects.all()
    serializer_class = HistoricoBuscaSerializer
