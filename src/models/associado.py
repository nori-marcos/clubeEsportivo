from datetime import date
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator

from src.models.types import Titularidade, TipoDePlano
from src.utils import formulario_utils


class Associado(BaseModel):
    id_associado: str = Field(default_factory=lambda: uuid4().hex)
    cpf: str
    nome: str = Field(min_length=1)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')
    telefone: str = Field(pattern=r'^\d+$', min_length=10, max_length=11)
    tipo: Titularidade
    plano: TipoDePlano
    data_nascimento: date | None
    endereco: str | None
    foto: bytes | None
    data_adesao: date = Field(default_factory=lambda: date.today())

    @field_validator('cpf')
    @classmethod
    def validar_cpf(cls, cpf_input: str) -> str:
        cpf = cpf_input.replace('.', '').replace('-', '')
        assert len(cpf) == 11 and cpf.isnumeric()
        return cpf

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, telefone_input: str) -> str:
        telefone = (telefone_input
                    .replace('(', '')
                    .replace(')', '')
                    .replace(' ', '')
                    .replace('-', ''))
        assert (10 <= len(telefone) <= 13) and telefone.isnumeric()
        return telefone

    @field_validator('data_nascimento', 'data_adesao')
    @classmethod
    def validar_datas(cls, data_input: str) -> date:
        return formulario_utils.tratar_data(data_input)

    @field_validator('foto', mode='before')
    @classmethod
    def validar_foto(cls, foto_input: str) -> bytes | None:
        return formulario_utils.tratar_data(foto_input)
