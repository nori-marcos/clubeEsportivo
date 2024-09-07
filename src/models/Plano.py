from pydantic import BaseModel

from src.models.types import TipoDePlano, Dinheiro


class Plano(BaseModel):
    nome: TipoDePlano
    valor: Dinheiro | None = None
