import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginSchema(BaseModel):
    """Schema para validação de login"""
    email: EmailStr = Field(...,
                            example="joao.silva@example.com")  # type: ignore
    password: str = Field(..., min_length=8,
                          example="SenhaSegura123!")  # type: ignore


class TokenResponseSchema(BaseModel):
    """Schema para resposta com tokens"""
    refresh: str
    access: str


class UserResponseSchema(BaseModel):
    """Schema para dados do usuário na resposta"""
    id: str
    nome: str
    email: str
    is_pcd: bool = False
    is_terceiro: bool = False
