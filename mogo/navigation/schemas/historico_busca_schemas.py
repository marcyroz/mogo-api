import uuid
import re
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class CriarHistoricoBuscaSchema(BaseModel):
    """Schema para histórico de buscas"""
    
    usuario_id: uuid.UUID = Field(...)
    origem_texto: str = Field(..., max_length=300, example="Casa")
    destino_texto: str = Field(..., max_length=300, example="Shopping Ibirapuera")
    
    # Dados do contexto da busca
    origem_lat: Optional[float] = Field(default=None)
    origem_lng: Optional[float] = Field(default=None)
    destino_lat: Optional[float] = Field(default=None)
    destino_lng: Optional[float] = Field(default=None)

    @model_validator(mode='after')
    def validar_textos_diferentes(self):
        """Origem e destino devem ter textos diferentes"""
        if self.origem_texto.lower().strip() == self.destino_texto.lower().strip():
            raise ValueError('Origem e destino devem ser diferentes')
        return self
