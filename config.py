import os

basedir = os.path.abspath(os.path.dirname(__file__))
POSTGRES_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:5432/db_clube_esportivo'

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', POSTGRES_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_APP = os.getenv('FLASK_APP', 'src')
