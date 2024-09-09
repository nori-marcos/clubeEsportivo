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
            sql_contrato = text("""
            INSERT INTO contratos (data_inicio, data_termino, plano)
            VALUES (CURRENT_DATE, CURRENT_DATE + INTERVAL '1 year', :plano)
            RETURNING id_contrato
            """)
            result_contrato = session.execute(sql_contrato, {'plano': associado.plano})
            id_contrato = result_contrato.scalar()

            sql_associado = text("""
            INSERT INTO associados (cpf, nome, foto, data_adesao, data_nascimento, endereco, email, associado_titular, contrato)
            VALUES (:cpf, :nome, :foto, CURRENT_DATE, :data_nascimento, :endereco, :email, :associado_titular, :contrato)
            RETURNING cpf
            """)

            result_associado = session.execute(sql_associado, {
                'cpf': associado.cpf.cpf,
                'nome': associado.nome,
                'foto': base64.b64decode(associado.foto) if associado.foto else None,
                'data_nascimento': associado.data_nascimento,
                'endereco': associado.endereco,
                'email': associado.email,
                'associado_titular': associado.associado_titular,
                'contrato': id_contrato
            })
            cpf_associado = result_associado.scalar()

            sql_telefones = text("""
            INSERT INTO associados_telefones (associado, telefone)
            VALUES (:associado, :telefone)
            """)
            for telefone in associado.telefones:
                session.execute(sql_telefones, {'associado': cpf_associado, 'telefone': telefone.telefone})

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
            cpf = associado.cpf.cpf

            sql_select = text("""
            SELECT nome, data_nascimento, endereco, email, associado_titular, contrato, foto, data_adesao
            FROM associados
            WHERE cpf = :cpf
            """)

            result = session.execute(sql_select, {'cpf': cpf})

            for row in result.mappings():
                nome = associado.nome if associado.nome else row['nome']
                data_nascimento = associado.data_nascimento if associado.data_nascimento else row['data_nascimento']
                endereco = associado.endereco if associado.endereco else row['endereco']
                email = associado.email if associado.email else row['email']
                contrato = row['contrato']
                foto = base64.b64decode(associado.foto) if associado.foto else None
                data_adesao = row['data_adesao']
                associado_titular = associado.associado_titular if associado.associado_titular is not None else None

                sql_update = text("""
                UPDATE associados
                SET nome = :nome, data_nascimento = :data_nascimento, endereco = :endereco, email = :email, associado_titular = :associado_titular, contrato = :contrato, foto = :foto, data_adesao = :data_adesao
                WHERE cpf = :cpf
                """)

                session.execute(sql_update, {
                    'cpf': cpf,
                    'nome': nome,
                    'data_nascimento': data_nascimento,
                    'endereco': endereco,
                    'email': email,
                    'associado_titular': associado_titular,
                    'contrato': contrato,
                    'foto': foto,
                    'data_adesao': data_adesao
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
                                             row['telefones'].split(', ')]
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
                    telefones=telefones
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
            session.execute(sql, {
                'cpf': cpf
            })
            session.commit()
            return True, "Associado removido com sucesso!"
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao remover o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")
