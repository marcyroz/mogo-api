from rest_framework import serializers
from social.models import Avaliacao, Favorito

class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'usuario', 'local', 'nota', 'comentario', 'created_at']
        
class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id', 'usuario', 'local', 'created_at']