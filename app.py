from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = 'postgresql+psycopg2://postgres:password@localhost:5432/dbClubeEsportivo'

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

app.config['SECRET_KEY'] = 'secret_key'

# Não tirar essa importação ou o Flask não vai conseguir encontrar as rotas
from routes import routes

if __name__ == '__main__':
    app.run(debug=True)
