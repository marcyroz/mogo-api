import uuid
import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CriarFavoritoSchema(BaseModel):
    """Schema para adicionar favoritos"""

    usuario_id: uuid.UUID = Field(...)
    local_id: uuid.UUID = Field(...)

    apelido: Optional[str] = Field(
        default=None,
        max_length=50,
        example="Meu hospital preferido"
    )

    @field_validator('apelido')
    @classmethod
    def validar_apelido_limpo(cls, v: Optional[str]) -> Optional[str]:
        if v:
            # Remove caracteres especiais desnecessários
            v = re.sub(r'[^\w\s-]', '', v).strip()
            if len(v) < 2:
                raise ValueError('Apelido deve ter pelo menos 2 caracteres')
        return v
