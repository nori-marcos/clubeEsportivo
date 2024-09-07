from pydantic import BaseModel


class Cargo(BaseModel):
    id_cargo: int | None = None
    nome: str
    descricao: str | None = None
    salario_base: float | None = None
