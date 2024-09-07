from datetime import date

from pydantic import BaseModel

from src.models.types import CPF


class Atestado(BaseModel):
    associado: CPF
    id_atestado: int
    data_emissao: date = None
    data_validade:date = None
    emitido_pelo_funcionario: CPF
