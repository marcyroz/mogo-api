from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from usuarios.models import Usuario
from django.contrib.gis.geos import Point
import uuid

# Rotas, Locais e Historico models


class Rota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='rotas')

    # Coordenadas de origem e destino
    origem_lat = models.FloatField()
    origem_lng = models.FloatField()
    destino_lat = models.FloatField()
    destino_lng = models.FloatField()

    # Geometria da rota (do seu diagrama)
    polyline_line = models.LineStringField()  # ← GeoDjango field!

    # Score de acessibilidade
    score_acessibilidade = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rotas'
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        ordering = ['-created_at']

        # Métodos do seu diagrama
    def calcular_score_acessibilidade(self):
        """Integração com YOLO Service"""
        # Implementação posterior
        pass

    def calcular_distancia_estimada(self):
        """Calcula distância estimada da rota em km"""
        origem = Point(self.origem_lng, self.origem_lat)
        destino = Point(self.destino_lng, self.destino_lat)
        return origem.distance(destino) * 111  # Aproximação para km

    def __str__(self):
        return f"Rota de {self.usuario.nome} - {self.created_at.strftime('%d/%m/%Y')}"


class Local(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()

    # GeoDjango field - combina lat/lng em um ponto
    point = models.PointField()  # ← GeoDjango field!

    tipo_local = models.CharField(max_length=50, choices=[
        ('saude', 'Saúde'),
        ('educacao', 'Educação'),
        ('transporte', 'Transporte'),
        ('comercio', 'Comércio'),
        ('lazer', 'Lazer'),
        ('servicos', 'Serviços'),
        ('religioso', 'Local Religioso'),
        ('cultural', 'Cultural'),
        ('outro', 'Outro'),
    ])

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'locais'
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'
        ordering = ['nome']

    def calcular_distancia_da(self, outra_coordenada):
        """Calcular distância de outro ponto"""
        outro_ponto = Point(outra_coordenada['lng'], outra_coordenada['lat'])
        return self.point.distance(outro_ponto)

    def get_avaliacoes_recentes(self, limite=5):
        """Retorna avaliações mais recentes"""
        return self.avaliacoes.order_by('-created_at')[:limite]

    def save(self, *args, **kwargs):
        """Atualizar point automaticamente baseado em lat/lng"""
        self.point = Point(self.longitude, self.latitude)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class HistoricoBusca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='historico_buscas')
    origem_texto = models.CharField(max_length=300)
    destino_texto = models.CharField(max_length=300)
    data_hora = models.DateTimeField(auto_now_add=True)

    # Coordenadas de origem e destino
    origem_lat = models.FloatField(null=True, blank=True, default=None)
    origem_lng = models.FloatField(null=True, blank=True, default=None)
    destino_lat = models.FloatField(null=True, blank=True, default=None)
    destino_lng = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'historico_buscas'
        verbose_name = 'Histórico de Busca'
        verbose_name_plural = 'Históricos de Busca'
        ordering = ['-data_hora']

    # Métodos do seu diagrama
    def visualizar_historico(self):
        """Retorna histórico do usuário"""
        return self.__class__.objects.filter(usuario=self.usuario).order_by('-data_hora')

    def selecionar_local(self, local):
        """Lógica para selecionar local do histórico"""
        # Implementação posterior
        pass

    def __str__(self):
        return f"{self.origem_texto} → {self.destino_texto}"
