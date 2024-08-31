from flask import render_template, session

from app import app
from controllers import associado_controller
from gateway.associado_gateway import AssociadoGateway


@app.route('/')
def index():
    form_data = session.pop('form_data', {})
    associados = AssociadoGateway.listar()
    return render_template('index.html', form_data=form_data, associados=associados)


@app.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()


@app.route('/editar/associado/<id_associado>', methods=['POST'])
def editar_associado(id_associado):
    return associado_controller.editar_associado(id_associado)
