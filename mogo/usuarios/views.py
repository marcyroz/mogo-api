# usuarios/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password


from usuarios.serializers import TerceiroSerializer
from usuarios.services import TerceiroService
from usuarios.exceptions.user_exceptions import TerceiroValidationError


from usuarios.models import Usuario, PCD, Terceiro
from usuarios.serializers import UsuarioSerializer, PCDSerializer, TerceiroSerializer
from usuarios.services import UsuarioService
from usuarios.exceptions.user_exceptions import (
    UsuarioValidationError,
    UsuarioJaExisteError,
    UsuarioNaoEncontradoError,
    ContaDesativadaError,
    AuthenticationRequiredError
)


class UsuarioViewSet(viewsets.ViewSet):
    """ViewSet completo para Usuário"""

    def list(self, request):
        """Listar usuários ativos"""
        usuarios = UsuarioService.listar_usuarios_ativos()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Criar usuário simples"""
        try:
            usuario = UsuarioService.criar_usuario(request.data)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=201)
        except (UsuarioValidationError, UsuarioJaExisteError) as e:
            return Response({"message": str(e.detail)}, status=e.status_code)

    def retrieve(self, request, pk=None):
        """Buscar usuário por ID"""
        try:
            resultado = UsuarioService.buscar_usuario_por_id(pk)
            usuario_data = dict(UsuarioSerializer(resultado['usuario']).data)
            usuario_data['pcd'] = resultado.get('pcd')
            return Response(usuario_data)
        except UsuarioNaoEncontradoError as e:
            return Response({"message": str(e.detail)}, status=e.status_code)

    @action(detail=True, methods=['put', 'patch'])
    def atualizar(self, request, pk=None):
        """Atualizar usuário"""
        try:
            usuario = UsuarioService.atualizar_usuario(pk, request.data)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except (UsuarioValidationError, UsuarioNaoEncontradoError, ContaDesativadaError) as e:
            return Response({"message": str(e.detail)}, status=e.status_code)


    @action(detail=True, methods=['delete'])
    def desativar(self, request, pk=None):
        try:
            UsuarioService.desativar_usuario(pk)
            return Response({"message": "Usuário desativado com sucesso."})
        except (UsuarioNaoEncontradoError, ContaDesativadaError) as e:
            return Response({"message": str(e.detail)}, status=e.status_code)
        except Exception as e:
            return Response({"message": "Erro inesperado: " + str(e)}, status=400)


    @action(detail=True, methods=['post'])
    def alterar_senha(self, request, pk=None):
        """
        Alterar senha do usuário.

        URL: /usuarios/usuario/<pk>/alterar_senha/
        """
        senha_atual = request.data.get("senha_atual")
        nova_senha = request.data.get("nova_senha")

        if not senha_atual or not nova_senha:
            return Response(
                {"message": "Campos 'senha_atual' e 'nova_senha' são obrigatórios."},
                status=400
            )

        try:
            # Chama o service existente que já valida senha atual e nova senha
            UsuarioService.alterar_senha(usuario_id=pk, senha_atual=senha_atual, nova_senha=nova_senha)
            return Response({"message": "Senha alterada com sucesso."}, status=200)

        except UsuarioNaoEncontradoError as e:
            return Response({"message": str(e.detail)}, status=e.status_code)
        except ContaDesativadaError as e:
            return Response({"message": str(e.detail)}, status=e.status_code)
        except AuthenticationRequiredError:
            return Response({"message": "Senha atual incorreta."}, status=400)
        except UsuarioValidationError as e:
            return Response({"message": "Nova senha inválida: " + str(e)}, status=400)
        except Exception as e:
            return Response({"message": "Erro inesperado: " + str(e)}, status=500)
        
    @action(detail=True, methods=['get'])
    def terceiros(self, request, pk=None):
        """
        Listar todos os terceiros vinculados a um usuário específico.
        URL: /usuarios/usuario/<pk>/terceiros/
        """
        try:
            # Filtrar todos os terceiros do usuário
            terceiros = TerceiroService.listar_terceiros().filter(usuario__id=pk)
            serializer = TerceiroSerializer(terceiros, many=True)
            return Response(serializer.data)
        except TerceiroValidationError as e:
            return Response({"message": str(e)}, status=404)
        except Exception as e:
            return Response({"message": "Erro inesperado: " + str(e)}, status=500)

class PCDViewSet(viewsets.ViewSet):
    """ViewSet para PCD como entidade fraca"""

    def list(self, request):
        """Listar todos os perfis PCD"""
        pcds = PCD.objects.all()
        serializer = PCDSerializer(pcds, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Buscar PCD por ID (usando o usuário como referência)"""
        try:
            # pk aqui é o ID do usuário dono do PCD
            pcd = PCD.objects.get(usuario__id=pk)
            serializer = PCDSerializer(pcd)
            return Response(serializer.data)
        except PCD.DoesNotExist:
            return Response({"message": "PCD não encontrado."}, status=404)

    def create(self, request):
        """Criar perfil PCD para um usuário já existente"""
        dados = request.data.get("pcd", {})
        usuario_id = dados.get("usuario_id")
        if not usuario_id:
            return Response({"message": "Campo 'usuario_id' é obrigatório."}, status=400)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuário não encontrado."}, status=404)

        # Checar se já existe PCD para este usuário
        if hasattr(usuario, "pcd"):
            return Response({"message": "PCD já existe para este usuário."}, status=400)

        # Criar PCD
        pcd = PCD(
            usuario=usuario,
            tipo_deficiencia=dados.get("tipo_deficiencia"),
            detalhes=dados.get("detalhes", "")
        )

        # Validar campos obrigatórios
        if not pcd.tipo_deficiencia:
            return Response({"message": "Campo 'tipo_deficiencia' é obrigatório."}, status=400)

        pcd.save()
        serializer = PCDSerializer(pcd)
        return Response(serializer.data, status=201)
    @action(detail=True, methods=['put', 'patch'])
    def atualizar(self, request, pk=None):
        """Atualizar PCD de um usuário"""
        try:
            pcd = PCD.objects.get(usuario__id=pk)
        except PCD.DoesNotExist:
            return Response({"message": "PCD não encontrado."}, status=404)

        dados = request.data
        if "tipo_deficiencia" in dados:
            pcd.tipo_deficiencia = dados["tipo_deficiencia"]
        if "detalhes" in dados:
            pcd.detalhes = dados["detalhes"]

        pcd.save()
        serializer = PCDSerializer(pcd)
        return Response(serializer.data)
class TerceiroViewSet(viewsets.ViewSet):
    """ViewSet para terceiros/cuidador"""

    def list(self, request):
        terceiros = TerceiroService.listar_terceiros()
        serializer = TerceiroSerializer(terceiros, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            terceiro = TerceiroService.buscar_por_id(pk)
            serializer = TerceiroSerializer(terceiro)
            return Response(serializer.data)
        except TerceiroValidationError as e:
            return Response({"message": str(e)}, status=404)

    def create(self, request):
        dados = request.data.get("terceiro", {})
        try:
            terceiro = TerceiroService.criar_terceiro(dados)
            serializer = TerceiroSerializer(terceiro)
            return Response(serializer.data, status=201)
        except TerceiroValidationError as e:
            return Response({"message": str(e)}, status=400)

    @action(detail=True, methods=['delete'])
    def deletar(self, request, pk=None):
        try:
            TerceiroService.deletar_terceiro(pk)
            return Response({"message": "Terceiro deletado com sucesso."})
        except TerceiroValidationError as e:
            return Response({"message": str(e)}, status=404)
    
    @action(detail=True, methods=['put', 'patch'])
    def atualizar(self, request, pk=None):
        """Atualizar terceiro"""
        try:
            terceiro = TerceiroService.atualizar_terceiro(pk, request.data)
            serializer = TerceiroSerializer(terceiro)
            return Response(serializer.data)
        except TerceiroValidationError as e:
            return Response({"message": str(e)}, status=404)