from pydantic import BaseModel


class Esporte(BaseModel):
    id_esporte: int | None = None
    nome: str | None = None
