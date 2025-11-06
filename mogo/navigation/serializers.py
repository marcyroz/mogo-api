from rest_framework import serializers
from django.contrib.gis.geos import LineString
from navigation.models import Rota, Local, HistoricoBusca

class RotaSerializer(serializers.ModelSerializer):
    polyline_points = serializers.ListField(
        child=serializers.ListField(child=serializers.FloatField()),
        required=False,
        write_only=True
    )
    
    class Meta:
        model = Rota
        fields = ['id', 'usuario', 'origem_lat', 'origem_lng', 'destino_lat', 'destino_lng', 'polyline_points', 'polyline_line', 'score_acessibilidade', 'created_at']
        read_only_fields = ['polyline_line', 'score_acessibilidade', 'created_at']
    
    def create(self, validated_data):
        polyline_points = validated_data.pop('polyline_points', None)
        
        if polyline_points and len(polyline_points) > 2:
            polyline_line = LineString(*polyline_points)
        else:
            polyline_line = LineString(
                (validated_data['origem_lng'], validated_data['origem_lat']),
                (validated_data['destino_lng'], validated_data['destino_lat'])
            )
        
        validated_data['polyline_line'] = polyline_line
        return super().create(validated_data)

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id', 'nome', 'latitude', 'longitude', 'point', 'tipo_local', 'created_at']
        
class HistoricoBuscaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricoBusca
        fields = ['id', 'usuario', 'origem_texto', 'destino_texto', 'data_hora']
