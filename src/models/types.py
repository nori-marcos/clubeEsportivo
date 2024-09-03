from enum import Enum


class TipoPlano(str, Enum):
    OURO = 'OURO'
    PRATA = 'PRATA'
    BRONZE = 'BRONZE'

class Titularidade(str, Enum):
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