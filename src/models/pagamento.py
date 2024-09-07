from datetime import date

from pydantic import BaseModel, Field

from src.models.types import StatusPagamento, Dinheiro


class Pagamento(BaseModel):
    contrato: int
    data_vencimento: date
    data_pagamento: date | None = None
    valor: Dinheiro
    status: StatusPagamento = StatusPagamento('PENDENTE')
