from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator


class CaseInsensitiveStrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value: Any):
        if isinstance(value, str):
            value = value.lower()

            for member in cls:
                if member.lower() == value:
                    return member
        return None

class TipoDePlano(CaseInsensitiveStrEnum):
    OURO = 'OURO'
    PRATA = 'PRATA'
    BRONZE = 'BRONZE'


class Titularidade(CaseInsensitiveStrEnum):
    TITULAR = 'TITULAR'
    DEPENDENTE = 'DEPENDENTE'


class StatusPagamento(CaseInsensitiveStrEnum):
    PENDENTE = 'PENDENTE'
    PAGO = 'PAGO'
    ATRASADO = 'ATRASADO'


class Dinheiro:
    def __init__(self, valor: float | str):
        if isinstance(valor, str):
            valor = float(valor)
        self.valor = valor

    def __str__(self):
        return f'{self.valor:.2f}'

class CPF(BaseModel):
    cpf: str

    @field_validator('cpf', mode='before')
    def validar_cpf(cls, cpf_input: str) -> str:
        cpf = (cpf_input
               .replace('.', '')
               .replace('-', ''))
        assert len(cpf) == 11 and cpf.isnumeric(), 'CPF deve ter 11 dígitos e ser numérico'
        return cpf

class Telefone(BaseModel):
    dono: CPF
    telefone: str

    @field_validator('telefone', mode='before')
    def validar_telefone(cls, telefone_input: str) -> str:
        telefone = (telefone_input
                    .replace('(', '')
                    .replace(')', '')
                    .replace(' ', '')
                    .replace('-', ''))
        assert (10 <= len(telefone) <= 13) and telefone.isnumeric(), 'Telefone inválido'
        return telefone
