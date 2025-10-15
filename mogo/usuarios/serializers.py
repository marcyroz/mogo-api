from rest_framework import serializers
from usuarios.models import Usuario, PCD, Terceiro

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'foto_perfil', 'created_at', 'deleted_at']

class PCDSerializer(serializers.ModelSerializer):
    # Apenas retorna o ID do usuário para manter comportamento de entidade fraca
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PCD
        fields = ['usuario', 'tipo_deficiencia', 'detalhes']

class TerceiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terceiro
        fields = ['id', 'usuario', 'relacao', 'descricao']
