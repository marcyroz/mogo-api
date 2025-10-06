import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

class CriarUsuarioSchema(BaseModel):
    """Schema para criação de usuário"""

    # Campos obrigatórios
    nome: str = Field(..., max_length=100, example="João Silva")
    sobrenome: str = Field(..., max_length=100, example="da Silva")
    email: EmailStr = Field(..., example="joao.silva@example.com")
    email_confirmation: EmailStr = Field(..., example="joao.silva@example.com")
    password: str = Field(..., min_length=8, example="SenhaSegura123!")
    password_confirmation: str = Field(...,
                                       min_length=8, example="SenhaSegura123!")

    # Campos opcionais
    foto_perfil: Optional[str] = Field(
        default=None, example="fotos_perfil/joao.png")
    bio: Optional[str] = Field(
        default=None, max_length=500, example="Apaixonado por tecnologia.")

    # Campos de aceitação de termos
    aceita_termos: bool = Field(..., example=True)
    aceita_privacidade: bool = Field(..., example=True)

    @model_validator(mode='after')
    def validar_confirmacoes(self):
        """Validações de confirmação"""
        if self.email != self.email_confirmation:
            raise ValueError('Email e confirmação devem ser idênticos')

        if self.password != self.password_confirmation:
            raise ValueError('Senha e confirmação devem ser idênticas')

        if not self.aceita_termos or not self.aceita_privacidade:
            raise ValueError(
                'Deve aceitar termos de uso e política de privacidade')

        return self

    @field_validator('nome', 'sobrenome')
    @classmethod
    def validar_nome_sobrenome(cls, v: str) -> str:
        if any(char.isdigit() for char in v):
            raise ValueError("Nome/sobrenome não pode conter números")

        if len(v.strip()) < 2:
            raise ValueError("Nome/sobrenome deve ter pelo menos 2 caracteres")

        if not re.match("^[a-zA-ZÀ-ÿ\s]*$", v):
            raise ValueError(
                "Nome/sobrenome deve conter apenas letras e espaços")

        return v.strip().title()

    @field_validator('password')
    @classmethod
    def validar_senha_forte(cls, v: str) -> str:
        """RNGC5 - Critérios mínimos de segurança"""
        if len(v) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve ter pelo menos 1 letra maiúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Senha deve ter pelo menos 1 número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Senha deve ter pelo menos 1 caractere especial')
        return v
