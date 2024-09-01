from enum import Enum


class TipoPlano(str, Enum):
    OURO = 'OURO'
    PRATA = 'PRATA'
    BRONZE = 'BRONZE'

class Titularidade(str, Enum):
    TITULAR = 'TITULAR'
    DEPENDENTE = 'DEPENDENTE'

