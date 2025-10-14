import hashlib
from pydantic import ValidationError
from django.db import IntegrityError
from django.db.models import Avg, Count

# Imports dos schemas
from .schemas.avaliacao_schemas import CriarAvaliacaoSchema
from .schemas.favorito_schemas import CriarFavoritoSchema

# Imports dos models
from .models import Avaliacao, Favorito

# Imports das exceptions customizadas
from .exceptions.social_exceptions import (
   AvaliacaoValidationError,
   AvaliacaoJaExisteError,
   AvaliacaoNaoEncontradaError,
   FavoritoValidationError,
   FavoritoJaExisteError,
   FavoritoNaoEncontradoError
)

class SocialService:
    """Service layer para operações sociais"""

    @staticmethod
    def criar_avaliacao(dados):
        """
        Criar nova avaliação
        """
        try:
            schema = CriarAvaliacaoSchema(**dados)
            
        except ValidationError as e:
            # Raise custom exception - global handler will process the details
            raise AvaliacaoValidationError()

        if Avaliacao.objects.filter(usuario_id=schema.usuario_id, local_id=schema.local_id).exists():
            raise AvaliacaoJaExisteError()

        avaliacao = Avaliacao.objects.create(**schema.dict())
        return avaliacao

    @staticmethod
    def criar_favorito(dados):
        """
        Criar novo favorito
        """
        try:
            schema = CriarFavoritoSchema(**dados)
            
        except ValidationError as e:
            # Raise custom exception - global handler will process the details
            raise FavoritoValidationError()

        if Favorito.objects.filter(usuario_id=schema.usuario_id, local_id=schema.local_id).exists():
            raise FavoritoJaExisteError()

        favorito = Favorito.objects.create(**schema.dict())
        return favorito

    @staticmethod
    def buscar_favorito(usuario_id, local_id):
        """
        Buscar favorito específico de um usuário para um local
        """
        try:
            favorito = Favorito.objects.get(usuario_id=usuario_id, local_id=local_id)
            return favorito
        except Favorito.DoesNotExist:
            raise FavoritoNaoEncontradoError()

    @staticmethod
    def listar_favoritos_usuario(usuario_id):
        """
        Listar todos os favoritos de um usuário
        """
        favoritos = Favorito.objects.filter(usuario_id=usuario_id).order_by('-created_at')
        return favoritos
        
    @staticmethod
    def buscar_avaliacao(usuario_id, local_id):
        """
        Buscar avaliação específica de um usuário para um local
        """
        try:
            avaliacao = Avaliacao.objects.get(usuario_id=usuario_id, local_id=local_id)
            return avaliacao
        except Avaliacao.DoesNotExist:
            raise AvaliacaoNaoEncontradaError()

    @staticmethod
    def listar_avaliacoes_usuario(usuario_id, limite=20):
        """
        Listar avaliações de um usuário
        """
        avaliacoes = Avaliacao.objects.filter(usuario_id=usuario_id).order_by('-created_at')[:limite]
        return avaliacoes

    @staticmethod
    def listar_avaliacoes_local(local_id, limite=10):
        """
        Listar avaliações de um local específico
        """
        avaliacoes = Avaliacao.objects.filter(local_id=local_id).order_by('-created_at')[:limite]
        return avaliacoes

    @staticmethod
    def remover_favorito(usuario_id, local_id):
        """
        Remover favorito de um usuário
        """
        try:
            favorito = Favorito.objects.get(usuario_id=usuario_id, local_id=local_id)
            favorito.delete()
            return True
        except Favorito.DoesNotExist:
            raise FavoritoNaoEncontradoError()

    @staticmethod
    def calcular_media_avaliacoes_local(local_id):
        """
        Calcular média das avaliações de um local
        """
        resultado = Avaliacao.objects.filter(local_id=local_id).aggregate(
            media=Avg('nota'),
            total_avaliacoes=Count('id')
        )
        
        return {
            'media_nota': round(resultado['media'], 1) if resultado['media'] else 0.0,
            'total_avaliacoes': resultado['total_avaliacoes']
        }