from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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
    """ViewSet para Usuário"""

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
        
    @action(detail=True, methods=['get'])
    def buscar(self, request, pk=None):
        """Buscar usuário por ID"""
        try:
            resultado = UsuarioService.buscar_usuario_por_id(pk)
            usuario_data = dict(UsuarioSerializer(resultado['usuario']).data)
            # Se não houver PCD, retorna None
            usuario_data['pcd'] = resultado.get('pcd')
            return Response(usuario_data)
        except UsuarioNaoEncontradoError as e:
            return Response({"message": str(e.detail)}, status=e.status_code)
        except Exception as e:
            # Captura qualquer outro erro e evita 500
            return Response({"message": "Erro inesperado: " + str(e)}, status=400)


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
        """Desativar conta (soft delete)"""
        try:
            UsuarioService.desativar_usuario(pk)
            return Response({"message": "Usuário desativado com sucesso."})
        except (UsuarioNaoEncontradoError, ContaDesativadaError) as e:
            return Response({"message": str(e.detail)}, status=e.status_code)


class PCDViewSet(viewsets.ViewSet):
    """ViewSet para PCD"""

    def create(self, request):
        """Criar perfil PCD para um usuário já existente"""
        from usuarios.models import Usuario, PCD
        from usuarios.serializers import PCDSerializer

        dados = request.data.get("pcd", {})

        # Checar se 'usuario_id' foi enviado
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
            forma_locomocao=dados.get("forma_locomocao"),
            recursos_acessibilidade=dados.get("recursos_acessibilidade", []),
            detalhes=dados.get("detalhes", "")
        )

        # Validar campos obrigatórios
        obrigatorios = ["tipo_deficiencia", "forma_locomocao", "recursos_acessibilidade"]
        for campo in obrigatorios:
            if not dados.get(campo):
                return Response({"message": f"Campo '{campo}' é obrigatório."}, status=400)

        pcd.save()
        serializer = PCDSerializer(pcd)
        return Response(serializer.data, status=201)


class TerceiroViewSet(viewsets.ViewSet):
    """ViewSet para Terceiro"""
    
    def create(self, request):
        """Endpoint ainda não implementado"""
        return Response({"message": "Endpoint para criação de terceiro ainda não implementado."}, status=501)
