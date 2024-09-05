from enum import Enum
from typing import Any


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

class StatusPagamento(str, Enum):
    PENDENTE = 'PENDENTE'
    PAGO = 'PAGO'
    ATRASADO = 'ATRASADO'

class MetodoPagamento(str, Enum):
    DEBITO = 'DEBITO'
    CREDITO = 'CREDITO'
    BOLETO = 'BOLETO'
    PIX = 'PIX'
    DINHEIRO = 'DINHEIRO'