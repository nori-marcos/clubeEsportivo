from datetime import datetime

from flask import flash, render_template, redirect, url_for, request

from src.gateway.associado_gateway import Gateway
from src.models.associado import Associado
from src.utils.arquivo_utils import processar_foto
from src.utils.formulario_utils import extrair_dados_formulario


def listar_associados():
    return Gateway.listar_associados()


def inserir_associado():
    try:
        foto = processar_foto(request.files.get('foto', None))
        associado = Associado(**request.form, foto=foto)
        sucesso, mensagem = Gateway.salvar_associado(associado)
        if sucesso:
            flash(mensagem, 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert')
        associados = Gateway.listar_associados()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def editar_associado():
    try:
        foto = processar_foto(request.files.get('foto', request.form.get('foto-atual', None)))
        associado = Associado(**request.form, foto=foto)
        sucesso, mensagem = Gateway.editar_associado(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit')
        associados = Gateway.listar_associados()
        today = datetime.today()
        return render_template('index.html', form_data=form_data, today=today, associados=associados)


def remover_associado(cpf):
    try:
        sucesso, mensagem = Gateway.remover_associado(cpf)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o associado: {e}', 'danger-remove')
        return redirect(url_for('main.index'))
