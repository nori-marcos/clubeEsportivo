from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from src.controllers import associado_controller
from src.main import bp


@bp.route('/')
def index():
    associados = associado_controller.listar_todos()
    today = datetime.today()
    return render_template('index.html', associados=associados, today=today, form_data={})


@bp.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()


@bp.route('/editar/associado/<id_associado>', methods=['POST'])
def editar_associado(id_associado):
    return associado_controller.editar_associado(id_associado)


@bp.route('/remover_associado/<id_associado>', methods=['GET', 'POST'])
def remover_associado(id_associado):
    if request.form.get('_method') == 'DELETE':
        return associado_controller.remover_associado(id_associado)
    flash('Método não permitido', 'danger')
    return redirect(url_for('main.index'))
