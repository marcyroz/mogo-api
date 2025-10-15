import hashlib
from pydantic import ValidationError
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import uuid
from pydantic import ValidationError
from django.db import IntegrityError
from usuarios.models import Usuario, Terceiro
from usuarios.schemas.terceiro_schema import CriarTerceiroSchema


# Imports dos schemas
from .schemas.user_schemas import CriarUsuarioSchema
from .schemas.pcd_schemas import CriarPCDSchema

# Imports dos models
from .models import Usuario, PCD
from usuarios.models import Usuario, PCD

# Imports das exceptions customizadas
from .exceptions.user_exceptions import (
    UsuarioValidationError,
    UsuarioJaExisteError,
    UsuarioNaoEncontradoError,
    ContaDesativadaError,
    AuthenticationRequiredError 
)

from usuarios.exceptions.user_exceptions import (
    UsuarioNaoEncontradoError,
    TerceiroJaExisteError,
    TerceiroValidationError
)

class UsuarioService:
    """Service layer para operações de usuário"""
    
    @staticmethod
    def criar_usuario(dados):
        """
        Criar novo usuário com validação completa
        
        Fluxo:
        1. Valida com Pydantic Schema
        2. Verifica se email já existe  
        3. Cria usuário no banco
        4. Retorna dados ou lança exception
        """
        try:
            schema = CriarUsuarioSchema(**dados)
            
        except ValidationError as e:
            raise UsuarioValidationError()
        
        # PASSO 2: Verificar se email já existe
        if Usuario.objects.filter(email=schema.email).exists():
            # 🚨 LANÇA EXCEPTION - Usuario já existe
            raise UsuarioJaExisteError()
        
        try:
            # Criar usuário no banco
            usuario = Usuario.objects.create(
                nome=f"{schema.nome} {schema.sobrenome}",  # Combinar nome e sobrenome
                email=schema.email,
                password=make_password(schema.password),
                bio=schema.bio,
                foto_perfil=schema.foto_perfil
            )
            
            # Retornar o objeto criado
            return usuario
            
        except IntegrityError:
            # PASSO 3B: Erro no banco (race condition)
            # Alguém criou o mesmo email entre a verificação e a criação
            raise UsuarioJaExisteError()

    @staticmethod
    def criar_usuario_pcd(dados_usuario, dados_pcd):
        """
        Criar usuário PCD (transação completa)
        
        Fluxo mais complexo com múltiplas validações
        """
        try:
            usuario_schema = CriarUsuarioSchema(**dados_usuario)
            
        except ValidationError as e:
            raise UsuarioValidationError()
        
        try:
            pcd_schema = CriarPCDSchema(**dados_pcd)
            
        except ValidationError as e:
            raise UsuarioValidationError()
        
        # PASSO 3: Verificar email único
        if Usuario.objects.filter(email=usuario_schema.email).exists():
            raise UsuarioJaExisteError()
        
        try:
            # Criar usuário
            usuario = Usuario.objects.create(
                nome=f"{usuario_schema.nome} {usuario_schema.sobrenome}",
                email=usuario_schema.email,
                password=make_password(usuario_schema.password),
                bio=usuario_schema.bio,
                foto_perfil=usuario_schema.foto_perfil
            )
            
            # PASSO 5: Criar perfil PCD
            pcd = PCD.objects.create(
                usuario=usuario,
                tipo_deficiencia=pcd_schema.tipo_deficiencia,
                forma_locomocao=pcd_schema.forma_locomocao,
                recursos_acessibilidade=pcd_schema.recursos_acessibilidade,
                detalhes=pcd_schema.detalhes
            )
            
            return {
                'usuario': usuario,
                'pcd': pcd
            }
            
        except IntegrityError:
            raise UsuarioJaExisteError()

    @staticmethod
    def autenticar_usuario(email, senha):
        """
        Autenticar usuário - exemplo de diferentes exceptions
        """
        try:
            # PASSO 1: Buscar usuário por email
            usuario = Usuario.objects.get(email=email)
            
        except Usuario.DoesNotExist:
            # PASSO 1B: Email não encontrado
            raise UsuarioNaoEncontradoError()
        
        # PASSO 2: Verificar se conta está ativa
        if usuario.deleted_at is not None:
            # PASSO 2B: Conta desativada
            raise ContaDesativadaError()
        
        # PASSO 3: Verificar senha
        if not check_password(senha, usuario.password):
            # Senha incorreta - tratamos como "não encontrado" por segurança
            raise UsuarioNaoEncontradoError()
        
        # PASSO 4: Usuário autenticado com sucesso
        # Verificar se tem perfil PCD
        is_pcd = False
        try:
            from models import PCD
            PCD.objects.get(usuario=usuario)
            is_pcd = True
        except PCD.DoesNotExist:
            pass
            
        return {
            'usuario': usuario,
            'is_pcd': is_pcd,
            'token': 'jwt-token-aqui'  # Implementar JWT depois
        }

    @staticmethod
    def buscar_usuario_por_id(usuario_id):
        """
        Buscar usuário - exemplo simples
        """
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Incluir dados PCD se existir
            dados_pcd = None
            try:
                pcd = PCD.objects.get(usuario=usuario)
                dados_pcd = {
                    'tipo_deficiencia': pcd.tipo_deficiencia,
                    'forma_locomocao': pcd.forma_locomocao,
                    'recursos_acessibilidade': getattr(pcd, 'recursos_acessibilidade', [])
                }
            except PCD.DoesNotExist:
                # Usuário não tem perfil PCD
                pass
            
            return {
                'usuario': usuario,
                'pcd': dados_pcd  
            }

        except Usuario.DoesNotExist:
            # 🚨 EXCEPTION vai para handler global
            raise UsuarioNaoEncontradoError()


    @staticmethod
    def atualizar_usuario(usuario_id, dados):
        """
        Atualizar usuário - exemplo de validação parcial
        """
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise UsuarioNaoEncontradoError()
        
        # Verificar se conta está ativa
        if usuario.deleted_at:
            raise ContaDesativadaError()
        
        # Atualizar campos permitidos
        if 'nome' in dados:
            if not dados['nome'] or len(dados['nome'].strip()) < 2:
                raise UsuarioValidationError()
            usuario.nome = dados['nome'].strip()
        

        
        if 'bio' in dados:
            if len(dados['bio']) > 500:
                raise UsuarioValidationError()
            usuario.bio = dados['bio']
        
        usuario.save()
        
        return usuario

    @staticmethod
    def desativar_usuario(usuario_id):
        """
        Desativar conta do usuário (soft delete)
        """
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            raise UsuarioNaoEncontradoError()
            
        if usuario.deleted_at:
            raise ContaDesativadaError()
        
        usuario.deleted_at = timezone.now()
        usuario.save()
        
        return True

    @staticmethod
    def listar_usuarios_ativos(limite=50):
        """
        Listar usuários ativos (para admin)
        """
        usuarios = Usuario.objects.filter(
            deleted_at__isnull=True
        ).order_by('-created_at')[:limite]
        
        return usuarios

    @staticmethod
    def alterar_senha(usuario_id, senha_atual, nova_senha):
        usuario = Usuario.objects.get(id=usuario_id)

        if usuario.deleted_at:
            raise ContaDesativadaError()

        if not check_password(senha_atual, usuario.password):
            raise AuthenticationRequiredError()

        # Validar senha mínima
        if len(nova_senha) < 8:
            raise UsuarioValidationError("Nova senha deve ter no mínimo 8 caracteres")

        usuario.password = make_password(nova_senha)
        usuario.save()
        return True



class TerceiroService:
    """Service layer para operações de terceiros/cuidador"""

    @staticmethod
    def criar_terceiro(dados):
        """
        Criar um terceiro/cuidador para uma PCD.
        """
        try:
            schema = CriarTerceiroSchema(**dados)
        except ValidationError as e:
            raise TerceiroValidationError(str(e))

        # Buscar usuário vinculado
        try:
            usuario = Usuario.objects.get(id=schema.usuario_id)
        except Usuario.DoesNotExist:
            raise UsuarioNaoEncontradoError()

        # Checar se já existe Terceiro com mesma relação para o usuário
        if Terceiro.objects.filter(usuario=usuario, relacao=schema.relacao).exists():
            raise TerceiroJaExisteError()

        try:
            terceiro = Terceiro.objects.create(
                usuario=usuario,
                relacao=schema.relacao,
                pcd_assistida_tipo_deficiencia=schema.pcd_assistida_tipo_deficiencia,
                descricao=schema.descricao
            )
            return terceiro

        except IntegrityError:
            raise TerceiroJaExisteError()

    @staticmethod
    def listar_terceiros():
        """Listar todos os terceiros"""
        return Terceiro.objects.all()

    @staticmethod
    def buscar_por_id(terceiro_id):
        """Buscar terceiro específico"""
        try:
            return Terceiro.objects.get(id=terceiro_id)
        except Terceiro.DoesNotExist:
            raise TerceiroValidationError("Terceiro não encontrado")

    @staticmethod
    def deletar_terceiro(terceiro_id):
        """Excluir terceiro"""
        try:
            terceiro = Terceiro.objects.get(id=terceiro_id)
            terceiro.delete()
            return True
        except Terceiro.DoesNotExist:
            raise TerceiroValidationError("Terceiro não encontrado")
        
    @staticmethod
    def atualizar_terceiro(terceiro_id, dados):
        """Atualizar um terceiro específico"""
        try:
            terceiro = Terceiro.objects.get(id=terceiro_id)
        except Terceiro.DoesNotExist:
            raise TerceiroValidationError("Terceiro não encontrado")

        # Atualizar campos permitidos
        if 'relacao' in dados:
            terceiro.relacao = dados['relacao']
        if 'descricao' in dados:
            terceiro.descricao = dados['descricao']

        terceiro.save()
        return terceiro
        
