from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field, field_validator

from src.models.types import Telefone, Dinheiro, CPF


class Funcionario(BaseModel):
    cpf: CPF
    nome: str | None = None
    data_nascimento: date | None = None
    data_admissao: date | None = None
    email: str = Field(pattern=r'^\S+@\S+\.\S+$', default=None)
    salario: Dinheiro | None = None
    endereco: str | None = None
    cargo: int
    departamento: int
    telefones: List[Telefone] = []


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
        return foto_input
