class Associado:
    def __init__(self, cpf, nome, email, telefone, tipo, plano, data_adesao, id_associado=None, data_nascimento=None,
                 endereco=None,
                 foto=None):
        self.id_associado = id_associado
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.tipo = tipo
        self.plano = plano
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.foto = foto
        self.data_adesao = data_adesao
