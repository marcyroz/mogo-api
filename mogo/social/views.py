# social/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Avaliacao, Favorito
from .serializers import AvaliacaoSerializer, FavoritoSerializer
from .services import SocialService
from .exceptions.social_exceptions import (
    AvaliacaoValidationError,
    AvaliacaoJaExisteError,
    AvaliacaoNaoEncontradaError,
    FavoritoValidationError,
    FavoritoJaExisteError,
    FavoritoNaoEncontradoError
)

# -----------------------------
# ViewSet completo para Avaliacao
# -----------------------------
class AvaliacaoViewSet(viewsets.ViewSet):
    """
    CRUD completo para Avaliação
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
        try:
            avaliacao = SocialService.criar_avaliacao(request.data)
            serializer = AvaliacaoSerializer(avaliacao)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AvaliacaoValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except AvaliacaoJaExisteError as e:
            return Response({'error': str(e)}, status=status.HTTP_409_CONFLICT)

    def retrieve(self, request, pk=None):
        try:
            avaliacao = Avaliacao.objects.get(pk=pk)
            serializer = AvaliacaoSerializer(avaliacao)
            return Response(serializer.data)
        except Avaliacao.DoesNotExist:
            return Response({'error': 'Avaliação não encontrada.'}, status=404)

    def update(self, request, pk=None):
        try:
            avaliacao = Avaliacao.objects.get(pk=pk)
            serializer = AvaliacaoSerializer(avaliacao, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Avaliacao.DoesNotExist:
            return Response({'error': 'Avaliação não encontrada.'}, status=404)

    def partial_update(self, request, pk=None):
        try:
            avaliacao = Avaliacao.objects.get(pk=pk)
            serializer = AvaliacaoSerializer(avaliacao, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Avaliacao.DoesNotExist:
            return Response({'error': 'Avaliação não encontrada.'}, status=404)

    def destroy(self, request, pk=None):
        try:
            avaliacao = Avaliacao.objects.get(pk=pk)
            avaliacao.delete()
            return Response(status=204)
        except Avaliacao.DoesNotExist:
            return Response({'error': 'Avaliação não encontrada.'}, status=404)

# -----------------------------
# ViewSet completo para Favorito
# -----------------------------
class FavoritoViewSet(viewsets.ViewSet):
    """
    CRUD completo para Favorito
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
        try:
            favorito = SocialService.criar_favorito(request.data)
            serializer = FavoritoSerializer(favorito)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except FavoritoValidationError as e:
            return Response({'error': str(e)}, status=400)
        except FavoritoJaExisteError as e:
            return Response({'error': str(e)}, status=409)

    def retrieve(self, request, pk=None):
        try:
            favorito = Favorito.objects.get(pk=pk)
            serializer = FavoritoSerializer(favorito)
            return Response(serializer.data)
        except Favorito.DoesNotExist:
            return Response({'error': 'Favorito não encontrado.'}, status=404)

    def update(self, request, pk=None):
        try:
            favorito = Favorito.objects.get(pk=pk)
            serializer = FavoritoSerializer(favorito, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Favorito.DoesNotExist:
            return Response({'error': 'Favorito não encontrado.'}, status=404)

    def partial_update(self, request, pk=None):
        try:
            favorito = Favorito.objects.get(pk=pk)
            serializer = FavoritoSerializer(favorito, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Favorito.DoesNotExist:
            return Response({'error': 'Favorito não encontrado.'}, status=404)

    def destroy(self, request, pk=None):
        try:
            favorito = Favorito.objects.get(pk=pk)
            favorito.delete()
            return Response(status=204)
        except Favorito.DoesNotExist:
            return Response({'error': 'Favorito não encontrado.'}, status=404)

    # Action customizada para buscar por usuario_id + local_id
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        usuario_id = request.query_params.get('usuario_id')
        local_id = request.query_params.get('local_id')
        if not usuario_id or not local_id:
            return Response({"message": "Parâmetros usuario_id e local_id são obrigatórios."}, status=400)

        favorito = SocialService.buscar_favorito(usuario_id, local_id)
        serializer = FavoritoSerializer(favorito)
        return Response(serializer.data)
