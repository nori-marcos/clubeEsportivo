from datetime import date

from pydantic import BaseModel, computed_field

from src.models.types import StatusPagamento, Dinheiro, CPF


class Pagamento(BaseModel):
    cpf: CPF
    nome: str
    associado_titular: str | None
    contrato: int
    data_vencimento: date
    data_pagamento: date | None = None
    valor: Dinheiro

    @computed_field
    def status(self) -> StatusPagamento:
        if self.data_vencimento >= date.today():
            if self.data_pagamento is None:
                return StatusPagamento('PENDENTE')
            else:
                return StatusPagamento('PAGO')
        else:
            return StatusPagamento('ATRASADO')
