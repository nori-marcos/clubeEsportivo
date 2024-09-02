from datetime import date
from uuid import uuid4

from pydantic import BaseModel, Field

from src.models.types import Titularidade, TipoPlano


class Associado(BaseModel):
    id_associado: str = Field(default_factory=lambda: uuid4().hex)
    cpf: str = Field(pattern=r'^\d+$', min_length=11, max_length=11)
    nome: str = Field(min_length=1)
    email: str
    telefone: str = Field(pattern=r'^\d+$', min_length=10, max_length=11)
    tipo: Titularidade
    plano: TipoPlano
    data_nascimento: date | None
    endereco: str | None
    foto: str | None
    data_adesao: date = Field(default_factory=lambda: date.today())
