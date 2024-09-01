import os

basedir = os.path.abspath(os.path.dirname(__file__))
DB_ACCOUNT = os.getenv('DB_ACCOUNT', 'clube_dba')
DB_PASSWORD = os.getenv('DB_PASSWORD', '1234567')
DB_URL = os.getenv('DB_URL', 'localhost:5432')
DB_NAME = os.getenv('DB_NAME', 'db_clube_esportivo')
POSTGRES_DATABASE_URI = os.getenv('POSTGRES_DATABASE_URI',
                                  f'postgresql+psycopg2://{DB_ACCOUNT}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', POSTGRES_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
