from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from src.controllers import associado_controller
from src.main import bp


@bp.route('/')
def index():
    associados = associado_controller.listar_associados()
    today = datetime.today()
    return render_template('index.html', associados=associados, today=today, form_data={})


@bp.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()


@bp.route('/editar/associado', methods=['POST'])
def editar_associado():
    return associado_controller.editar_associado()


@bp.route('/remover_associado/<cpf_associado>', methods=['GET', 'POST'])
def remover_associado(cpf_associado):
    if request.form.get('_method') == 'DELETE':
        return associado_controller.remover_associado(cpf_associado)
    flash('Método não permitido', 'danger')
    return redirect(url_for('main.index'))
