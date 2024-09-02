from datetime import datetime

from flask import flash, render_template, redirect, url_for

from src.gateway.associado_gateway import AssociadoGateway
from src.utils.formulario_utils import criar_associado_pelo_formulario, extrair_dados_formulario


def inserir_associado():
    try:
        associado = criar_associado_pelo_formulario()
        sucesso, mensagem = AssociadoGateway.salvar(associado)
        if sucesso:
            flash(mensagem, 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert')
        associados = AssociadoGateway.listar()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def editar_associado(id_associado):
    try:
        associado = criar_associado_pelo_formulario(id_associado)
        sucesso, mensagem = AssociadoGateway.editar(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario(id_associado)
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit')
        associados = AssociadoGateway.listar()
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
