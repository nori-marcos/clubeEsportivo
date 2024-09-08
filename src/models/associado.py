from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, field_validator

from src.models.types import Titularidade, TipoDePlano, Telefone, CPF, StatusAssociado
from src.utils.arquivo_utils import validar_foto_base64


class Associado(BaseModel):
    cpf: CPF
    nome: str = Field(min_length=1)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')
    tipo: Titularidade
    plano: TipoDePlano
    data_nascimento: date | None
    endereco: str | None
    foto: str | None = Field(default=None)
    data_adesao: date = Field(default_factory=lambda: date.today())
    status: StatusAssociado | None = Field(default=None)
    telefones: List[Telefone] = Field(default_factory=list)
    associado_titular: str | None = Field(default=None)

    @field_validator('data_nascimento', 'data_adesao', mode='before')
    def validar_datas(cls, data_input) -> date:
        if isinstance(data_input, date):
            return data_input
        if isinstance(data_input, str):
            try:
                return datetime.strptime(data_input, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(data_input.split(' ')[0], '%Y-%m-%d').date()
                except ValueError:
                    raise AssertionError('Data inválida')
        raise AssertionError('Data inválida')

    @field_validator('foto', mode='before')
    def validar_foto(cls, foto_input: str | None) -> str | None:
        if validar_foto_base64(foto_input):
            return foto_input
        return None
