from datetime import date
from uuid import uuid4

from pydantic import BaseModel, Field

from src.models.types import StatusPagamento, MetodoPagamento


class Pagamento(BaseModel):
    id_pagamento: str = Field(default_factory=lambda: uuid4().hex)
    id_associado: str = Field(default_factory=lambda: uuid4().hex)
    valor: float
    metodo: MetodoPagamento
    data_pagamento: date | None = Field()
    data_vencimento: date
    status: StatusPagamento
