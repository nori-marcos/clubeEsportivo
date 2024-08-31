from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost:5432/dbClubeEsportivo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Não tirar essa importação ou o Flask não vai conseguir encontrar as rotas
from routes import routes

if __name__ == '__main__':
    app.run(debug=True)
