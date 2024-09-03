import uuid

from sqlalchemy import create_engine
from sqlalchemy import text, Table, Column, String, Date, MetaData, UUID, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

import config
from src.exceptions.exceptions import CustomException
from src.models.associado import Associado
from src.models.types import TipoDePlano, Titularidade

engine = create_engine(config.POSTGRES_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


class AssociadoGateway:
    metadata = MetaData()
    associados_table = Table(
        'Associados', metadata,
        Column('ID_Associado', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        Column('Cpf', String(200), unique=True, nullable=False),
        Column('Nome', String(200), nullable=False),
        Column('Data_Nascimento', Date),
        Column('Endereco', String(200)),
        Column('Telefone', String(15)),
        Column('Email', String(50)),
        Column('Tipo', String(50), nullable=False),
        Column('Plano', String(50), nullable=False),
        Column('Foto', Text),
        Column('Data_Adesao', Date, nullable=False)
    )
    metadata.create_all(engine)

    @staticmethod
    def salvar(associado: Associado):
        try:
            sql = text("""
            INSERT INTO "Associados" ("ID_Associado", "Cpf", "Nome", "Data_Nascimento", "Endereco", "Telefone", "Email", "Tipo", "Plano", "Foto", "Data_Adesao")
            VALUES (:ID_Associado, :Cpf, :Nome, :Data_Nascimento, :Endereco, :Telefone, :Email, :Tipo, :Plano, :Foto, :Data_Adesao)
            RETURNING "ID_Associado"
            """)
            result = session.execute(sql, {
                'ID_Associado': associado.id_associado,
                'Cpf': associado.cpf,
                'Nome': associado.nome,
                'Data_Nascimento': associado.data_nascimento,
                'Endereco': associado.endereco,
                'Telefone': associado.telefone,
                'Email': associado.email,
                'Tipo': associado.tipo,
                'Foto': associado.foto,
                'Data_Adesao': associado.data_adesao,
                'Plano': associado.plano
            })
            session.commit()
            associado.id_associado = result.scalar()
            return True, "Associado inserido com sucesso!"
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao salvar o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")

    @staticmethod
    def editar(associado):
        try:
            sql = text("""
            UPDATE "Associados"
            SET "Cpf" = :Cpf, "Nome" = :Nome, "Data_Nascimento" = :Data_Nascimento, "Endereco" = :Endereco, "Telefone" = :Telefone, "Email" = :Email, "Tipo" = :Tipo, "Plano" = :Plano, "Foto" = :Foto, "Data_Adesao" = :Data_Adesao
            WHERE "ID_Associado" = :ID_Associado
            """)
            session.execute(sql, {
                'ID_Associado': associado.id_associado,
                'Cpf': associado.cpf,
                'Nome': associado.nome,
                'Data_Nascimento': associado.data_nascimento,
                'Endereco': associado.endereco,
                'Telefone': associado.telefone,
                'Email': associado.email,
                'Tipo': associado.tipo,
                'Foto': associado.foto,
                'Data_Adesao': associado.data_adesao,
                'Plano': associado.plano
            })
            session.commit()
            return True, "Associado atualizado com sucesso!"

        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao editar o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")

    @staticmethod
    def listar_todos():
        try:
            sql = text("""
            SELECT "ID_Associado", "Cpf", "Nome", "Data_Nascimento", "Endereco", "Telefone", "Email", "Tipo", "Plano", "Foto", "Data_Adesao" 
            FROM "Associados"
            """)
            result = session.execute(sql)
            associados = []
            for row in result.mappings():
                associado = Associado(
                    id_associado=str(row['ID_Associado']),
                    cpf=row['Cpf'],
                    nome=row['Nome'],
                    email=row['Email'],
                    telefone=row['Telefone'],
                    tipo=Titularidade(row['Tipo']),
                    data_nascimento=row['Data_Nascimento'],
                    endereco=row['Endereco'],
                    foto=row['Foto'],
                    data_adesao=row['Data_Adesao'],
                    plano=TipoDePlano(row['Plano'])
                )
                associados.append(associado)
            return associados
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao listar os associados: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")

    @staticmethod
    def remover(id_associado):
        try:
            sql = text("""
            DELETE FROM "Associados"
            WHERE "ID_Associado" = :ID_Associado
            """)
            session.execute(sql, {
                'ID_Associado': id_associado
            })
            session.commit()
            return True, "Associado removido com sucesso!"
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao editar o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")
