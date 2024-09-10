from datetime import date

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.exceptions.exceptions import CustomException
from src.gateway import session_singleton
from src.gateway.config.tables_config import check_and_create_database
from src.models.pagamento import Pagamento

session = session_singleton
check_and_create_database(session)

class Pagamento_Gateway:
    @staticmethod
    def listar_pagamentos(cpf: str, data: date = None):
        sql = """
        SELECT
        a.cpf AS cpf_associado,
        a.nome AS nome_associado,
        a.contrato,
        p.data_vencimento,
        p.data_pagamento,
        p.valor
        FROM pagamentos p
        LEFT JOIN associados a ON p.contrato = a.contrato
        LEFT JOIN contratos c ON c.id_contrato = a.contrato
        WHERE a.associado_titular = :cpf_titular
        """
        dto = {'cpf': cpf}
        if date:
            sql += ' AND p.data_vencimento = :data_vencimento'
            dto['data_vencimento'] = date

        try:
            result = session.execute(text(sql), dto)
            pagamentos = []
            for row in result.mappings():
                pagamento = {
                    'cpf': row['cpf'],
                    'nome': row['nome'],
                    'associado_titular': row['associado_titular'],
                    'contrato': row['contrato'],
                    'data_vencimento': row['data_vencimento'],
                    'data_pagamento': row['data_pagamento'],
                    'valor': row['valor'],
                }
                pagamentos.append(pagamento)
            return pagamentos
        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao listar os pagamentos: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")


    @staticmethod
    def editar_pagamento(pagamento: Pagamento):
        try:
            sql = text("""
            UPDATE pagamentos
            SET valor = :valor, data_pagamento = :data_pagamento
            WHERE contrato = :contrato AND data_vencimento = :data_vencimento
            """)

            session.execute(sql, {
                'contrato': pagamento.contrato,
                'data_vencimento': pagamento.data_vencimento,
                'valor': pagamento.valor,
                'data_pagamento': pagamento.data_pagamento,
            })
            session.commit()
            return True, "Pagamento atualizado com sucesso!"

        except SQLAlchemyError as e:
            session.rollback()
            erro_original = getattr(e, 'orig', None)
            if erro_original:
                raise CustomException(f"Erro ao editar o associado: {erro_original}")
            else:
                raise CustomException(f"Erro no banco de dados: {e}")
