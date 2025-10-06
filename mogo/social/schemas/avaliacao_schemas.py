import uuid
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class CriarAvaliacaoSchema(BaseModel):
    """Schema para criação de avaliações"""

    usuario_id: uuid.UUID = Field(...)
    local_id: uuid.UUID = Field(...)
    nota: int = Field(..., ge=1, le=5, example=5)
    comentario: Optional[str] = Field(
        default=None,
        max_length=1000,
        example="Local muito acessível, com rampa e elevador funcionando"
    )

    @model_validator(mode='after')
    def validar_comentario_obrigatorio_nota_extrema(self):
        """Notas 1 ou 5 devem ter comentário para serem mais úteis"""
        if self.nota in [1, 5] and not self.comentario:
            if self.nota == 1:
                raise ValueError(
                    'Avaliações com nota 1 devem incluir um comentário explicando os problemas')
            else:
                raise ValueError(
                    'Avaliações com nota 5 devem incluir um comentário detalhando os pontos positivos')
        return self
