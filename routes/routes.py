from flask import render_template

from app import app
from controllers import associado_controller


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()
