import re


class Associado:
    def __init__(self, cpf, nome, email, telefone, tipo, plano, data_adesao, id_associado=None, data_nascimento=None,
                 endereco=None, foto=None):
        self.id_associado = id_associado
        self.cpf = cpf
        self.nome = self.validar_nome(nome)
        self.email = email
        self.telefone = telefone
        self.tipo = self.validar_tipo(tipo)
        self.plano = self.validar_plano(plano)
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.foto = foto
        self.data_adesao = self.validar_data_adesao(data_adesao)

    @staticmethod
    def validar_cpf(cpf):
        pattern = r'^\d{3}\.\d{3}\.\d{3}\-\d{2}$'
        if not re.match(pattern, cpf):
            raise ValueError("CPF inválido")
        return cpf

    @staticmethod
    def validar_nome(nome):
        if not nome:
            raise ValueError("Nome não pode ser vazio")
        return nome

    @staticmethod
    def validar_tipo(tipo):
        if tipo not in ["titular", "dependente"]:
            raise ValueError("Tipo deve ser 'titular' ou 'dependente'")
        return tipo

    @staticmethod
    def validar_plano(plano):
        if plano not in ["ouro", "prata", "bronze"]:
            raise ValueError("Plano deve ser 'ouro', 'prata' ou 'bronze'")
        return plano

    @staticmethod
    def validar_data_adesao(data_adesao):
        if not data_adesao:
            raise ValueError("Data de Adesão é obrigatória")
        return data_adesao
