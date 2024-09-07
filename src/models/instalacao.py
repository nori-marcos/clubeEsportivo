from datetime import date

from pydantic import BaseModel, Field, field_validator

from src.models.types import Titularidade, Plano


class Instalacao(BaseModel):
    id_instalacao: int | None = None
    em_funcionamento: bool = Field(default=False)
    capacidade: int = Field(default=0)
