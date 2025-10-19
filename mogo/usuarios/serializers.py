from rest_framework import serializers
from usuarios.models import Usuario, PCD, Terceiro


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email',
                  'foto_perfil', 'created_at', 'deleted_at']


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


# ADICIONAR ESTE SERIALIZER
class RegisterInputSerializer(serializers.Serializer):
    """Serializer para a interface do DRF no endpoint de register"""
    nome = serializers.CharField(max_length=100, help_text="Nome do usuário")
    sobrenome = serializers.CharField(
        max_length=100, help_text="Sobrenome do usuário")
    email = serializers.EmailField(help_text="Email do usuário")
    email_confirmation = serializers.EmailField(
        help_text="Confirmação do email")
    password = serializers.CharField(
        min_length=8, write_only=True, help_text="Senha (mínimo 8 caracteres)")
    password_confirmation = serializers.CharField(
        min_length=8, write_only=True, help_text="Confirmação da senha")
    bio = serializers.CharField(
        max_length=500, required=False, allow_blank=True, help_text="Biografia do usuário")
    foto_perfil = serializers.CharField(
        required=False, allow_blank=True, help_text="URL da foto de perfil")
    aceita_termos = serializers.BooleanField(
        help_text="Aceita os termos de uso")
    aceita_privacidade = serializers.BooleanField(
        help_text="Aceita a política de privacidade")


# ADICIONAR ESTE SERIALIZER
class LoginInputSerializer(serializers.Serializer):
    """Serializer para a interface do DRF no endpoint de login"""
    email = serializers.EmailField(help_text="Email do usuário")
    password = serializers.CharField(
        write_only=True, help_text="Senha do usuário")


class TokenSerializer(serializers.Serializer):
    """Serializer para tokens JWT"""
    refresh = serializers.CharField()
    access = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    """Serializer para resposta de login"""
    message = serializers.CharField()
    user = serializers.DictField()
    tokens = TokenSerializer()


class RegisterResponseSerializer(serializers.Serializer):
    """Serializer para resposta de registro"""
    message = serializers.CharField()
    user = serializers.DictField()
    tokens = TokenSerializer()
