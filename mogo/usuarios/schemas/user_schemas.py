import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator


class CriarUsuarioSchema(BaseModel):
    id: uuid.UUID = Field(..., default_factory=uuid.uuid4)
    nome: str = Field(..., max_length=100, example="João Silva")
    email: EmailStr = Field(..., example="joao.silva@example.com")
    password: str = Field(..., min_length=8, example="SenhaSegura123!")
    password_repeat: str = Field(..., min_length=8, example="SenhaSegura123!")
    tipo_deficiencia: str = Field(
        ..., regex=r'^(fisica|visual|auditiva|intelectual|multipla)$', example="fisica")
    foto_perfil: str | None = Field(
        default=None, example="fotos_perfil/joao.png")
    bio: str | None = Field(default=None, max_length=500,
                            example="Apaixonado por tecnologia e inclusão.")
    created_at: datetime = Field(..., default_factory=datetime.now)
    deleted_at: datetime | None = Field(default=None)

    @validator('nome')
    def validar_nome(cls, v):
        # Verifica se tem numeros
        if any(char.isdigit() for char in v):
            raise ValueError("Nome não pode conter números")

        # Verifica tamanho mínimo
        if len(v.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")

        # Verifica caracteres especiais
        if not re.match("^[a-zA-ZÀ-ÿ\s]*$", v):
            raise ValueError("Nome deve conter apenas letras e espaços")

        return v.strip()  # Remove espaços extras
