from django.shortcuts import render
# views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from social.models import Avaliacao, Favorito
from social.serializers import AvaliacaoSerializer, FavoritoSerializer
from social.services import SocialService
from social.exceptions.social_exceptions import (
    AvaliacaoValidationError,
    AvaliacaoJaExisteError,
    AvaliacaoNaoEncontradaError,
    FavoritoValidationError,
    FavoritoJaExisteError,
    FavoritoNaoEncontradoError
)


class AvaliacaoViewSet(viewsets.ViewSet):
    """
    ViewSet para Avaliação
    """

    def list(self, request):
        usuario_id = request.query_params.get('usuario_id')
        local_id = request.query_params.get('local_id')

        if usuario_id and local_id:
            avaliacao = SocialService.buscar_avaliacao(usuario_id, local_id)
            serializer = AvaliacaoSerializer(avaliacao)
            return Response(serializer.data)

        elif usuario_id:
            avaliacoes = SocialService.listar_avaliacoes_usuario(usuario_id)
        elif local_id:
            avaliacoes = SocialService.listar_avaliacoes_local(local_id)
        else:
            avaliacoes = Avaliacao.objects.all()

        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        return Response(serializer.data)

    def create(self, request):
        avaliacao = SocialService.criar_avaliacao(request.data)
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data, status=201)


class FavoritoViewSet(viewsets.ViewSet):
    """
    ViewSet para Favorito
    """

    def list(self, request):
        usuario_id = request.query_params.get('usuario_id')
        if usuario_id:
            favoritos = SocialService.listar_favoritos_usuario(usuario_id)
        else:
            favoritos = Favorito.objects.all()

        serializer = FavoritoSerializer(favoritos, many=True)
        return Response(serializer.data)

    def create(self, request):
        favorito = SocialService.criar_favorito(request.data)
        serializer = FavoritoSerializer(favorito)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        usuario_id = request.query_params.get('usuario_id')
        local_id = request.query_params.get('local_id')
        if not usuario_id or not local_id:
            return Response(
                {"message": "Parâmetros usuario_id e local_id são obrigatórios."},
                status=400
            )
        favorito = SocialService.buscar_favorito(usuario_id, local_id)
        serializer = FavoritoSerializer(favorito)
        return Response(serializer.data)
