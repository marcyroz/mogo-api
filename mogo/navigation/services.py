from pydantic import ValidationError
from django.db import IntegrityError
from django.contrib.gis.geos import Point, LineString
from django.contrib.gis.db.models.functions import Distance

# Imports dos schemas
from schemas.historico_busca_schemas import CriarHistoricoBuscaSchema
from schemas.local_schemas import CriarLocalSchema
from schemas.rota_schema import CriarRotaSchema

# Imports dos models
from models import HistoricoBusca, Local, Rota

# Imports das exceptions customizadas
from exceptions.navigation_exceptions import (
    LocalNaoEncontradoError,
    LocalValidationError,
    LocalJaExisteError,
    RotaValidationError,
    RotaNaoEncontradaError,
    CoordenadaInvalidaError,
    HistoricoBuscaValidationError,
)

class NavigationService:
    """Service layer para operações de navegação"""

    @staticmethod
    def criar_local(dados):
        """
        Criar novo local
        """
        try:
            schema = CriarLocalSchema(**dados)
            
        except ValidationError as e:
            raise LocalValidationError()

        # Verificar se já existe um local muito próximo (mesmo ponto basicamente)
        ponto_novo = Point(schema.longitude, schema.latitude)
        locais_proximos = Local.objects.annotate(
            distancia=Distance('point', ponto_novo)
        ).filter(distancia__lt=0.01)  # Menos de 10 metros
        
        if locais_proximos.exists():
            raise LocalJaExisteError()

        local = Local.objects.create(**schema.dict())
        return local

    @staticmethod
    def criar_rota(dados):
        """
        Criar nova rota
        """
        try:
            schema = CriarRotaSchema(**dados)
            
        except ValidationError as e:
            raise RotaValidationError()

        # Validar se as coordenadas são válidas (dentro do Brasil ou área de interesse)
        if not NavigationService._validar_coordenadas_brasil(
            schema.origem_lat, schema.origem_lng, 
            schema.destino_lat, schema.destino_lng
        ):
            raise CoordenadaInvalidaError()

        # Criar geometria da linha da rota
        origem_point = Point(schema.origem_lng, schema.origem_lat)
        destino_point = Point(schema.destino_lng, schema.destino_lat)
        polyline = LineString(origem_point, destino_point)

        # Criar rota com dados do schema + geometria
        dados_rota = schema.dict()
        dados_rota['polyline_line'] = polyline

        rota = Rota.objects.create(**dados_rota)
        return rota

    @staticmethod
    def criar_historico_busca(dados):
        """
        Criar novo histórico de busca
        """
        try:
            schema = CriarHistoricoBuscaSchema(**dados)
            
        except ValidationError as e:
            raise HistoricoBuscaValidationError()

        historico = HistoricoBusca.objects.create(**schema.dict())
        return historico

    @staticmethod
    def buscar_local(local_id):
        """
        Buscar local por ID
        """
        try:
            local = Local.objects.get(id=local_id)
            return local
        except Local.DoesNotExist:
            raise LocalNaoEncontradoError()
        
    @staticmethod
    def buscar_rota(rota_id):
        """
        Buscar rota por ID
        """
        try:
            rota = Rota.objects.get(id=rota_id)
            return rota
        except Rota.DoesNotExist:
            raise RotaNaoEncontradaError()

    @staticmethod
    def buscar_locais_proximos(latitude, longitude, raio_km=5):
        """
        Buscar locais próximos a uma coordenada
        """
        try:
            ponto_referencia = Point(longitude, latitude)
            
            # Converter km para graus (aproximação)
            raio_graus = raio_km / 111.0
            
            locais = Local.objects.annotate(
                distancia=Distance('point', ponto_referencia)
            ).filter(
                distancia__lt=raio_graus
            ).order_by('distancia')
            
            return locais
            
        except Exception:
            raise CoordenadaInvalidaError()

    @staticmethod
    def buscar_rotas_usuario(usuario_id, limite=10):
        """
        Buscar rotas de um usuário
        """
        rotas = Rota.objects.filter(
            usuario_id=usuario_id
        ).order_by('-created_at')[:limite]
        
        return rotas

    @staticmethod
    def buscar_historico_usuario(usuario_id, limite=20):
        """
        Buscar histórico de buscas de um usuário
        """
        historico = HistoricoBusca.objects.filter(
            usuario_id=usuario_id
        ).order_by('-data_hora')[:limite]
        
        return historico

    @staticmethod
    def calcular_rota_otimizada(origem_lat, origem_lng, destino_lat, destino_lng):
        """
        Calcular rota otimizada considerando acessibilidade
        """
        # Validar coordenadas
        if not NavigationService._validar_coordenadas_brasil(
            origem_lat, origem_lng, destino_lat, destino_lng
        ):
            raise CoordenadaInvalidaError()

        # Aqui seria a integração com serviços de roteamento
        # Por enquanto, retorna dados básicos
        origem_point = Point(origem_lng, origem_lat)
        destino_point = Point(destino_lng, destino_lat)
        
        # Calcular distância aproximada
        distancia_km = origem_point.distance(destino_point) * 111
        
        return {
            'origem': {'lat': origem_lat, 'lng': origem_lng},
            'destino': {'lat': destino_lat, 'lng': destino_lng},
            'distancia_estimada_km': round(distancia_km, 2),
            'geometria': LineString(origem_point, destino_point),
            'score_acessibilidade': 0.0  # Será calculado pelo serviço YOLO
        }

    @staticmethod
    def _validar_coordenadas_brasil(origem_lat, origem_lng, destino_lat, destino_lng):
        """
        Validar se as coordenadas estão dentro do Brasil (validação básica)
        """
        # Limites aproximados do Brasil
        BRASIL_LAT_MIN, BRASIL_LAT_MAX = -34.0, 6.0
        BRASIL_LNG_MIN, BRASIL_LNG_MAX = -74.0, -32.0
        
        coordenadas = [
            (origem_lat, origem_lng),
            (destino_lat, destino_lng)
        ]
        
        for lat, lng in coordenadas:
            if not (BRASIL_LAT_MIN <= lat <= BRASIL_LAT_MAX and
                    BRASIL_LNG_MIN <= lng <= BRASIL_LNG_MAX):
                return False
                
        return True