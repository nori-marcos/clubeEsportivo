from flask import render_template, session, request, flash, redirect, url_for

from app import app
from controllers import associado_controller
from gateway.associado_gateway import AssociadoGateway


@app.route('/')
def index():
    form_data = session.pop('form_data', {})
    associados = AssociadoGateway.listar()

    erro = request.args.get('error')
    if erro:
        flash(erro, 'danger')

    return render_template('index.html', form_data=form_data, associados=associados)


@app.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()


@app.route('/editar/associado/<id_associado>', methods=['POST'])
def editar_associado(id_associado):
    return associado_controller.editar_associado(id_associado)


@app.route('/remover_associado/<id_associado>', methods=['GET', 'POST'])
def remover_associado(id_associado):
    if request.form.get('_method') == 'DELETE':
        return associado_controller.remover_associado(id_associado)
    flash('Método não permitido', 'danger')
    return redirect(url_for('index'))
