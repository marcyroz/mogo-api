import uuid
from typing import Optional
from pydantic import BaseModel, Field


class CriarTerceiroSchema(BaseModel):
    """Schema para terceiro/cuidador"""

    usuario_id: uuid.UUID = Field(...)

    # RNGN5 - Identificação como cuidador/terceiro
    relacao: str = Field(
        ...,
        pattern=r'^(familiar|cuidador|amigo|voluntario|outro)$',
        example="familiar"
    )

    # Informações sobre a PCD assistida
    pcd_assistida_tipo_deficiencia: str = Field(
        ...,
        pattern=r'^(fisica|visual|auditiva|intelectual|multipla)$',
        example="fisica"
    )

    descricao: Optional[str] = Field(
        default=None,
        max_length=500,
        example="Sou mãe de uma pessoa com deficiência visual"
    )
