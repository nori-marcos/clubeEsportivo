import os

from sqlalchemy import text


def check_and_create_database(session):
    sql_verifica_tabelas = text("""
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='public';
    """)

    result = session.execute(sql_verifica_tabelas)

    tabelas = [row[0] for row in result]

    if not tabelas:
        sql_criar_tabelas_path = os.path.join(os.path.dirname(__file__), '../../../db/PostgreSQL.sql')
        sql_popular_tabelas_path = os.path.join(os.path.dirname(__file__), '../../../db/Mock.sql')

        with open(sql_criar_tabelas_path, 'r') as sql_criar_tabelas:
            sql_criar_tabelas = sql_criar_tabelas.read()
            session.execute(text(sql_criar_tabelas))

        with open(sql_popular_tabelas_path, 'r') as sql_popular_tabelas:
            sql_popular_tabelas = sql_popular_tabelas.read()
            session.execute(text(sql_popular_tabelas))

        session.commit()
