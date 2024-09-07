from pydantic import BaseModel


class Departamento(BaseModel):
    id_departamento: int | None = None
    localizacao: int | None = None
    nome: str
