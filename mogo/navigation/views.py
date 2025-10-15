# navigation/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Rota, Local, HistoricoBusca
from .serializers import RotaSerializer, LocalSerializer, HistoricoBuscaSerializer

class RotaViewSet(viewsets.ModelViewSet):
    queryset = Rota.objects.all()
    serializer_class = RotaSerializer

    @action(detail=False, methods=['delete'])
    def deletar_por_usuario(self, request):
        """
        Deleta todas as rotas de um usuário pelo usuario_id
        """
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({"error": "usuario_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        registros = Rota.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response({"message": f"{count} rotas deletadas"}, status=status.HTTP_200_OK)


class LocalViewSet(viewsets.ModelViewSet):
    queryset = Local.objects.all()
    serializer_class = LocalSerializer

    @action(detail=False, methods=['delete'])
    def deletar_por_usuario(self, request):
        """
        Deleta todos os locais de um usuário pelo usuario_id
        """
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({"error": "usuario_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        registros = Local.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response({"message": f"{count} locais deletados"}, status=status.HTTP_200_OK)


class HistoricoBuscaViewSet(viewsets.ModelViewSet):
    queryset = HistoricoBusca.objects.all()
    serializer_class = HistoricoBuscaSerializer

    @action(detail=False, methods=['delete'])
    def deletar_por_usuario(self, request):
        """
        Deleta todos os históricos de busca de um usuário pelo usuario_id
        """
        usuario_id = request.query_params.get('usuario_id')
        if not usuario_id:
            return Response({"error": "usuario_id é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        registros = HistoricoBusca.objects.filter(usuario_id=usuario_id)
        count = registros.count()
        registros.delete()
        return Response({"message": f"{count} registros deletados"}, status=status.HTTP_200_OK)
