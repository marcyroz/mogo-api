from django.db import models
from usuarios.models import Usuario
from navigation.models import Local
import uuid

# Avaliacao e Favoritos models


class Avaliacao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='avaliacoes')
    local = models.ForeignKey(
        Local, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField()  # 1 a 5
    comentario = models.TextField(null=True, blank=True, max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'avaliacoes'
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(nota__gte=1) & models.Q(nota__lte=5),
                name='valid_nota_range'
            ),
            models.UniqueConstraint(
                fields=['usuario', 'local'],
                name='unique_usuario_local_avaliacao'
            )
        ]

    def __str__(self):
        return f"Avaliação de {self.usuario.nome} para {self.local.nome} - {self.nota} estrelas"


class Favorito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='favoritos')
    local = models.ForeignKey(
        Local, on_delete=models.CASCADE, related_name='favoritos')
    apelido = models.CharField(
        max_length=50, null=True, blank=True)  # Apelido opcional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favoritos'
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        ordering = ['-created_at']
        unique_together = ('usuario', 'local')

    def __str__(self):
        return f"{self.usuario.nome} favoritou {self.local.nome}"
