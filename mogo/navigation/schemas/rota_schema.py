import uuid
from pydantic import BaseModel, Field, model_validator


class CriarRotaSchema(BaseModel):
    """Schema para criação de rotas"""

    usuario_id: uuid.UUID = Field(...)
    origem_lat: float = Field(..., ge=-90, le=90, example=-23.5505)
    origem_lng: float = Field(..., ge=-180, le=180, example=-46.6333)
    destino_lat: float = Field(..., ge=-90, le=90, example=-23.5600)
    destino_lng: float = Field(..., ge=-180, le=180, example=-46.6400)

    @model_validator(mode='after')
    def validar_coordenadas_diferentes(self):
        """Origem e destino devem ser diferentes"""
        if (abs(self.origem_lat - self.destino_lat) < 0.0001 and
                abs(self.origem_lng - self.destino_lng) < 0.0001):
            raise ValueError('Origem e destino devem ser diferentes')
        return self
