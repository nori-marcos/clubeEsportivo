from datetime import date

from pydantic import BaseModel, Field

from src.models.types import StatusPagamento, MetodoPagamento


class Pagamento(BaseModel):
    cpf_associado: str
    nome_associado: str
    valor: float
    metodo: MetodoPagamento
    data_pagamento: date | None = Field()
    data_vencimento: date
    status: StatusPagamento
