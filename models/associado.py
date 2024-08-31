import uuid

from app import db


class Associado:
    def __init__(self, cpf, nome, email, telefone, plano):
        self.id = str(uuid.uuid4())
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.plano = plano

    def save(self):
        sql = f"""
        INSERT INTO members (id, cpf, name, email, telefone, plano)
        VALUES ('{self.id}', '{self.cpf}', '{self.nome}', '{self.email}', '{self.telefone}', '{self.plano}');
        """
        db.engine.execute(sql)
