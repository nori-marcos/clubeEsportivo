from datetime import datetime

from flask import flash, render_template, redirect, url_for, request

from src.gateway.associado_gateway import AssociadoGateway
from src.models.associado import Associado
from src.utils.arquivo_utils import processar_foto
from src.utils.formulario_utils import extrair_dados_formulario


def listar_todos():
    return AssociadoGateway.listar_todos()


def inserir_associado():
    try:
        foto = processar_foto(request.files.get('foto', None))
        associado = Associado(**request.form, foto=foto)
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


def editar_associado():
    try:
        foto = processar_foto(request.files.get('foto', request.form.get('foto-atual', None)))
        associado = Associado(**request.form, foto=foto)
        sucesso, mensagem = AssociadoGateway.editar(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit')
        associados = AssociadoGateway.listar_todos()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def remover_associado(cpf):
    try:
        sucesso, mensagem = AssociadoGateway.remover(cpf)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o associado: {e}', 'danger-remove')
        return redirect(url_for('main.index'))
