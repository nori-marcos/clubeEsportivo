import base64
from datetime import date
from typing import List

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions.exceptions import CustomException
from src.gateway import session_singleton
from src.gateway.config.tables_config import check_and_create_database
from src.models.associado import Associado
from src.models.types import Titularidade, TipoDePlano, CPF, Telefone

session = session_singleton
check_and_create_database(session)


class Gateway:
    @staticmethod
    def salvar_associado(associado: Associado):
        try:
            sql_contrato_associado_telefones = text("""
            CALL salvar_contrato_associado_telefone(:cpf, :nome, :email, :plano, 
            :data_nascimento, :endereco, :foto, :telefones, :associado_titular)
            """)

            session.execute(sql_contrato_associado_telefones, {
                'cpf': associado.cpf.cpf,
                'nome': associado.nome,
                'email': associado.email,
                'plano': associado.plano,
                'data_nascimento': associado.data_nascimento,
                'endereco': associado.endereco,
                'foto': base64.b64decode(associado.foto) if associado.foto else None,
                'telefones': [telefone.telefone for telefone in associado.telefones],
                'associado_titular': associado.associado_titular if associado.associado_titular else None
            })
            session.commit()
            return True, "Associado inserido com sucesso!"
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao inserir o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")

    @staticmethod
    def editar_associado(associado):
        try:
            sql = text("""
            CALL editar_contrato_associado_telefone(:cpf, :nome, :email, :plano,
            :data_nascimento, :endereco, :foto, :telefones, :associado_titular)
            """)

            session.execute(sql, {
                'cpf': associado.cpf.cpf,
                'nome': associado.nome,
                'email': associado.email,
                'plano': associado.plano,
                'data_nascimento': associado.data_nascimento,
                'endereco': associado.endereco,
                'foto': base64.b64decode(associado.foto) if associado.foto else None,
                'telefones': [telefone.telefone for telefone in associado.telefones],
                'associado_titular': associado.associado_titular if associado.associado_titular else None
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
    def listar_associados():
        try:
            sql = text("""
            SELECT
            a.cpf,
            a.nome AS nome_associado,
            a.foto,
            a.data_adesao,
            a.data_nascimento,
            a.endereco,
            a.email,
            a.associado_titular,
            a.contrato,
            STRING_AGG(t.telefone, ', ') AS telefones,
            p.nome AS nome_plano
            FROM associados a
            LEFT JOIN associados_telefones t ON a.cpf = t.associado
            LEFT JOIN contratos c ON a.contrato = c.id_contrato
            LEFT JOIN planos p ON c.plano = p.nome
            GROUP BY 
            a.cpf, 
            a.nome, 
            a.foto, 
            a.data_adesao, 
            a.data_nascimento, 
            a.endereco, 
            a.email,
            a.associado_titular, 
            a.contrato,
            p.nome
            ORDER BY a.nome
            """)

            result = session.execute(sql)
            associados = []
            for row in result.mappings():
                cpf: CPF = CPF(cpf=row['cpf'])
                nome: str = row['nome_associado']
                email: str = row['email']
                tipo: Titularidade = Titularidade.DEPENDENTE if row['associado_titular'] else Titularidade.TITULAR
                plano: TipoDePlano = TipoDePlano(row['nome_plano'].upper())
                data_nascimento: date = row['data_nascimento']
                endereco: str = row['endereco']
                foto_memoryview = row['foto']
                foto_base64: str = base64.b64encode(foto_memoryview).decode('utf-8') if foto_memoryview else None
                data_adesao: date = row['data_adesao']
                telefones: List[Telefone] = [Telefone(dono=cpf, telefone=numero.strip()) for numero in
                                             row['telefones'].split(', ')] if row['telefones'] else []
                associado_titular = row['associado_titular']
                associado = Associado(
                    cpf=cpf,
                    nome=nome,
                    email=email,
                    tipo=tipo,
                    plano=plano,
                    data_nascimento=data_nascimento,
                    endereco=endereco,
                    foto=foto_base64,
                    data_adesao=data_adesao,
                    telefones=telefones,
                    associado_titular=associado_titular
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
    def remover_associado(cpf):
        try:
            sql = text("""
            DELETE FROM associados
            WHERE cpf = :cpf
            """)
            session.execute(sql, {'cpf': cpf})
            session.commit()
            return True, "Associado removido com sucesso!"
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao remover o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")
