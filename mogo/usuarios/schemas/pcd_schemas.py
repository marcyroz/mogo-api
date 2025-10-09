import uuid
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class CriarPCDSchema(BaseModel):
    """Schema para PCD - baseado nas RNGs do questionário"""

    usuario_id: uuid.UUID = Field(...)

    # RNGN7 - Campo obrigatório
    tipo_deficiencia: str = Field(
        ...,
        pattern=r'^(fisica|visual|auditiva|intelectual|multipla)$',
        example="fisica"
    )

    # RNGN8/RNGN9 - Campo livre se não encontrar na lista
    deficiencia_personalizada: Optional[str] = Field(
        default=None,
        max_length=200,
        example="Deficiência específica não listada"
    )

    # RNGN10 - Como se locomove (obrigatório)
    forma_locomocao: str = Field(
        ...,
        example="cadeira_rodas"
    )

    # RNGN13/RNGN14 - Recursos de acessibilidade (múltipla escolha)
    recursos_acessibilidade: List[str] = Field(
        ...,
        min_length=1,  # RNGN16
        example=["rampas", "pisos_tateis", "elevadores"]
    )

    detalhes: Optional[str] = Field(
        default=None,
        max_length=1000,
        example="Detalhes adicionais sobre minha deficiência"
    )

    @model_validator(mode='after')
    def validar_recursos_outros(self):
        """RNGN15 - Se selecionou 'outros', campo deve ser preenchido"""
        if "outros" in self.recursos_acessibilidade and not self.outros_recursos:
            raise ValueError(
                'Ao selecionar "outros recursos", descreva-os no campo adicional')
        return self
