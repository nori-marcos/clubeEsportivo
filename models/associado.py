import uuid

import psycopg2
from sqlalchemy import text, Table, Column, String, MetaData
from sqlalchemy.exc import IntegrityError

from app import session, engine


class Associado:
    # Garante que a tabela associados exista no banco de dados
    __tablename__ = 'associados'
    metadata = MetaData()
    associados_table = Table(
        __tablename__, metadata,
        Column('id', String(36), primary_key=True),
        Column('cpf', String(11), unique=True, nullable=False),
        Column('nome', String(80), nullable=False),
        Column('email', String(120), unique=True, nullable=False),
        Column('telefone', String(20), nullable=False),
        Column('plano', String(50), nullable=False)
    )
    metadata.create_all(engine)

    # Construtor da classe
    def __init__(self, cpf, nome, email, telefone, plano):
        self.id = str(uuid.uuid4())
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.plano = plano

    def save(self):
        try:
            sql = text("""
            INSERT INTO associados (id, cpf, nome, email, telefone, plano)
            VALUES (:id, :cpf, :nome, :email, :telefone, :plano)
            """)

            session.execute(sql, {
                'id': self.id,
                'cpf': self.cpf,
                'nome': self.nome,
                'email': self.email,
                'telefone': self.telefone,
                'plano': self.plano
            })
            session.commit()
            return True, "Associado inserido com sucesso!"
        except IntegrityError as e:
            session.rollback()
            if isinstance(e.orig, psycopg2.errors.UniqueViolation):
                return False, f"{e.orig}"
        return False, f"Ocorreu um erro: {e}"
