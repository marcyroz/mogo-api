from rest_framework import serializers
from navigation.models import Rota, Local, HistoricoBusca

class RotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rota
        fields = ['id', 'usuario', 'origem_lat', 'origem_lng', 'destino_lat', 'destino_lng', 'polyline_line', 'score_acessibilidade', 'created_at']
        
class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id', 'nome', 'latitude', 'longitude', 'point', 'TIPO_LOCAL', 'created_at']
        
class HistoricoBuscaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoBusca
        fields = ['id', 'usuario', 'origem_texto', 'destino_texto', 'data_hora']