from pydantic import BaseModel, Field


class CriarLocalSchema(BaseModel):
    """Schema para cadastro de locais"""

    nome: str = Field(..., min_length=2, max_length=200,
                      example="Hospital das Clínicas")
    latitude: float = Field(..., ge=-90, le=90, example=-23.5505)
    longitude: float = Field(..., ge=-180, le=180, example=-46.6333)

    tipo_local: str = Field(
        ...,
        pattern=r'^(saude|educacao|transporte|comercio|lazer|servicos|religioso|cultural|outro)$',
        example="saude"
    )
    