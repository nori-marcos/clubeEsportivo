from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from src.models.types import Titularidade, TipoDePlano


class Associado(BaseModel):
    cpf: str = Field(pattern=r'^\d+$', min_length=11, max_length=11)
    nome: str = Field(min_length=1)
    email: str = Field(pattern=r'^\S+@\S+\.\S+$')
    telefone: str = Field(pattern=r'^\d+$', min_length=10, max_length=11)
    tipo: Titularidade
    plano: TipoDePlano
    data_nascimento: date | None
    endereco: str | None
    foto: str | None = Field(default=None)
    data_adesao: date = Field(default_factory=lambda: date.today())

    @field_validator('cpf', mode='before')
    def validar_cpf(cls, cpf_input: str) -> str:
        cpf = (cpf_input
               .replace('.', '')
               .replace('-', ''))
        assert len(cpf) == 11 and cpf.isnumeric(), 'CPF deve ter 11 dígitos e ser numérico'
        return cpf

    @field_validator('telefone', mode='before')
    def validar_telefone(cls, telefone_input: str) -> str:
        telefone = (telefone_input
                    .replace('(', '')
                    .replace(')', '')
                    .replace(' ', '')
                    .replace('-', ''))
        assert (10 <= len(telefone) <= 13) and telefone.isnumeric(), 'Telefone inválido'
        return telefone

    @field_validator('data_nascimento', 'data_adesao', mode='before')
    def validar_datas(cls, data_input) -> date:
        if isinstance(data_input, date):
            return data_input
        if isinstance(data_input, str):
            try:
                return datetime.strptime(data_input, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.strptime(data_input.split(' ')[0], '%Y-%m-%d').date()
                except ValueError:
                    raise AssertionError('Data inválida')
        raise AssertionError('Data inválida')

    @field_validator('tipo', mode='before')
    def validar_tipo(cls, tipo_input: str) -> Titularidade:
        titularidade = Titularidade(tipo_input.upper())
        assert titularidade in Titularidade.__members__.values(), 'Tipo inválido'
        return titularidade

    @field_validator('plano', mode='before')
    def validar_plano(cls, plano_input: str) -> TipoDePlano:
        tipo_plano = TipoDePlano(plano_input.upper())
        assert tipo_plano in TipoDePlano.__members__.values(), 'Plano inválido'
        return tipo_plano

    @field_validator('foto', mode='before')
    def validar_foto(cls, foto_input: str | None) -> str | None:
        return foto_input
