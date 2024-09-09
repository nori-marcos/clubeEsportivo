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

            caminho_fotos = os.path.join(os.path.dirname(__file__), '../../../db/photos')

            fotos = {
                'simone': os.path.join(caminho_fotos, 'Simone Beatriz da Luz.jpeg'),
                'ester': os.path.join(caminho_fotos, 'Ester Regina da Rocha.jpeg'),
                'tania': os.path.join(caminho_fotos, 'Tânia Sara da Luz.jpeg'),
                'marcia': os.path.join(caminho_fotos, 'Márcia Maya Almada.png'),
                'isaac': os.path.join(caminho_fotos, 'Isaac Erick Dias.png'),
                'joao': os.path.join(caminho_fotos, 'João Pedro da Silva.png')
            }

            fotos_bytes = {}
            for nome, caminho in fotos.items():
                with open(caminho, 'rb') as foto_file:
                    fotos_bytes[nome] = foto_file.read()

            sql_upload_photo = text("""
            UPDATE associados
            SET foto = :simone
            WHERE contrato = 1;
            
            UPDATE associados
            SET foto = :ester
            WHERE contrato = 2;
            
            UPDATE associados
            SET foto = :tania
            WHERE contrato = 3;
            
            UPDATE associados
            SET foto = :marcia
            WHERE contrato = 4;
            
            UPDATE associados
            SET foto = :isaac
            WHERE contrato = 5;
            
            UPDATE associados
            SET foto = :joao
            WHERE contrato = 6;
            """)

            session.execute(sql_upload_photo, fotos_bytes)
            session.commit()
