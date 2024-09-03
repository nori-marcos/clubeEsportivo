from datetime import datetime

from flask import flash, render_template, redirect, url_for, request

from src.gateway.associado_gateway import AssociadoGateway
from src.models.associado import Associado
from src.utils.formulario_utils import extrair_dados_formulario


def listar_todos():
    return AssociadoGateway.listar_todos()


def inserir_associado():
    try:
        associado = Associado(**request.form)
        sucesso, mensagem = AssociadoGateway.salvar(associado)
        if sucesso:
            flash(mensagem, 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert')
        associados = AssociadoGateway.listar_todos()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def editar_associado(id_associado):
    try:
        associado = Associado(**request.form)
        sucesso, mensagem = AssociadoGateway.editar(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario(id_associado)
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit')
        associados = AssociadoGateway.listar_todos()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def remover_associado(id_associado):
    try:
        sucesso, mensagem = AssociadoGateway.remover(id_associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o associado: {e}', 'danger-remove')
        return redirect(url_for('main.index'))
