from pydantic import BaseModel


class Equipe(BaseModel):
    id_equipe: int | None = None
    nome: str | None = None
    esporte_praticado: int
