from django.db import models
import uuid
from pydantic import BaseModel, model_validator
from typing_extensions import Self

# Usuario, PCD e Terceiro models


class Usuario(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    password_repeat = models.CharField(max_length=128)
    foto_perfil = models.ImageField(
        upload_to='fotos_perfil/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('A senha não coincide.')
        return self

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['nome']),
        ]
        constraints = [                          # Segurança
            models.CheckConstraint(
                check=models.Q(deleted_at__isnull=True) |
                models.Q(deleted_at__gte=models.F('created_at')),
                name='valid_deletion_date'
            )
        ]

    def __str__(self):
        return self.nome


class PCD(models.Model):

    TIPOS_DEFICIENCIA = [
        ('fisica', 'Física'),
        ('visual', 'Visual'),
        ('auditiva', 'Auditiva'),
        ('intelectual', 'Intelectual'),
        ('multipla', 'Múltipla'),
    ]

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='pcd')
    tipo_deficiencia = models.CharField(
        max_length=20,
        choices=TIPOS_DEFICIENCIA
    )
    detalhes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'pcds'
        verbose_name = 'Pessoa com Deficiência'
        verbose_name_plural = 'Pessoas com Deficiência'
        ordering = ['tipo_deficiencia']

    def __str__(self):
        return f"PCD - {self.usuario.nome}"


class Terceiro(models.Model):

    TIPOS_RELACAO = [
        ('familiar', 'Familiar'),
        ('cuidador', 'Cuidador Profissional'),
        ('amigo', 'Amigo'),
        ('voluntario', 'Voluntário'),
        ('outro', 'Outro'),
    ]

    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name='terceiro')
    relacao = models.CharField(max_length=20, choices=TIPOS_RELACAO)
    descricao = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'terceiros'
        verbose_name = 'Terceiro Responsável'
        verbose_name_plural = 'Terceiros Responsáveis'
        ordering = ['relacao']

    def __str__(self):
        return f"Terceiro - {self.usuario.nome}"
