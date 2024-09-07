from datetime import date

from pydantic import BaseModel


class Evento(BaseModel):
    id_evento: int | None = None
    nome: str
    data: date
    descricao: str | None = None
