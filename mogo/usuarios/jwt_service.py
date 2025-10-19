from rest_framework_simplejwt.tokens import RefreshToken
from typing import cast, Any

from usuarios.models import PCD, Terceiro, Usuario 


class TokenService:
    """Service responsável por gerenciar tokens JWT"""

    @staticmethod
    def gerar_tokens(usuario: Usuario) -> dict:
        """
        Gera tokens JWT customizados com informações adicionais do usuário

        Args:
            usuario: Instância do modelo Usuario
        Returns:
            dict com 'refresh' e 'access' tokens
        """
        refresh = RefreshToken.for_user(cast(Any, usuario))

        # Adicionar claims customizados ao token
        refresh['email'] = usuario.email  # Remover duplicação
        refresh['nome'] = usuario.nome
        refresh['user_id'] = str(usuario.id)

        # Verificar se é PCD
        is_pcd = PCD.objects.filter(usuario=usuario).exists()
        refresh['is_pcd'] = is_pcd

        # Verificar se é Terceiro
        is_terceiro = Terceiro.objects.filter(usuario=usuario).exists()
        refresh['is_terceiro'] = is_terceiro

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
