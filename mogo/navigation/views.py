from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from analysis.tasks import processar_rota_async
from .models import Rota, Local, HistoricoBusca
from .serializers import RotaSerializer, LocalSerializer, HistoricoBuscaSerializer
from analysis.services import processar_acessibilidade_rota_em_ram
from .services import NavigationService
import os
import uuid


class RotaViewSet(viewsets.ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Override create para usar NavigationService"""
        dados = request.data.copy()
        dados["usuario_id"] = str(request.user.id)

        try:
            rota = NavigationService.criar_rota(dados)
            # ENVIAR PARA CELERY (async)
            processar_rota_async.delay(str(rota.id))

            serializer = self.get_serializer(rota)
            return Response(
                {
                    **serializer.data,
                    "status": "processando",
                    "message": "Rota criada. Acessibilidade sendo processada em background.",
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def status(self, request, pk=None):
        """Consulta status detalhado do processamento"""
        rota = self.get_object()

        # Se processou, retorna detalhes completos
        resposta = {
            "id": str(rota.id),
            "status_processamento": rota.status_processamento,
            "score_acessibilidade": rota.score_acessibilidade,
            "concluido": rota.status_processamento == "concluido",
        }

        # Se tem erro
        if rota.erro_mensagem:
            resposta["erro"] = rota.erro_mensagem

        return Response(resposta)

    @action(detail=False, methods=["delete"])
    def deletar_por_usuario(self, request):
        usuario_id = request.query_params.get("usuario_id")
        if not usuario_id:
            return Response(
                {"error": "usuario_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        registros = Rota.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response(
            {"message": f"{count} rotas deletadas"}, status=status.HTTP_200_OK
        )

    @action(detail=True, methods=["post"])
    def avaliar_acessibilidade(self, request, pk=None):
        rota = self.get_object()
        api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
        resultado = processar_rota_async.delay(str(rota.id))
        return Response({"task_id": resultado.id, "status": "processando"}, status=200)


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

    @action(detail=False, methods=["delete"])
    def deletar_por_usuario(self, request):
        usuario_id = request.query_params.get("usuario_id")
        if not usuario_id:
            return Response(
                {"error": "usuario_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        registros = Local.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response(
            {"message": f"{count} locais deletados"}, status=status.HTTP_200_OK
        )


class HistoricoBuscaViewSet(viewsets.ModelViewSet):
    queryset = HistoricoBusca.objects.all()
    serializer_class = HistoricoBuscaSerializer

    @action(detail=False, methods=["delete"])
    def deletar_por_usuario(self, request):
        usuario_id = request.query_params.get("usuario_id")
        if not usuario_id:
            return Response(
                {"error": "usuario_id é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        registros = HistoricoBusca.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response(
            {"message": f"{count} registros deletados"}, status=status.HTTP_200_OK
        )
