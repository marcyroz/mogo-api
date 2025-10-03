from rest_framework import serializers
from usuarios.models import Usuario, PCD, Terceiro

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'foto_perfil', 'created_at',  'deleted_at']
        
class PCDSerializer(serializers.ModelSerializer):
    class Meta:
        model = PCD
        fields = ['usuario', 'tipo_deficiencia', 'detalhes']
        
class TerceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terceiro
        fields = ['usuario','relacao', 'descricao']