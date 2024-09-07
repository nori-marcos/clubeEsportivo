from datetime import datetime

from flask import flash, render_template, redirect, url_for, request

from src.gateway.gateway import Gateway
from src.models.associado import Associado
from src.models.types import CPF, Telefone
from src.utils.arquivo_utils import processar_foto
from src.utils.formulario_utils import extrair_dados_formulario


def listar_associados():
    return Gateway.listar_associados()


def inserir_associado():
    try:
        foto = processar_foto(request.files.get('foto', None))
        telefone1_form = request.form.get('telefone1', None)
        telefone1: Telefone = Telefone(telefone=telefone1_form, cpf=request.form.get('cpf')) if telefone1_form else None
        telefone2_form = request.form.get('telefone2', None)
        telefone2: Telefone = Telefone(telefone=telefone2_form, cpf=request.form.get('cpf')) if telefone2_form else None
        telefones = [telefone1, telefone2] if telefone1 or telefone2 else []
        associado = Associado(**request.form, foto=foto, telefones=telefones)
        sucesso, mensagem = Gateway.salvar_associado(associado)
        if sucesso:
            flash(mensagem, 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert-member')
        associados = Gateway.listar_associados()
        pagamentos = Gateway.listar_pagamentos()
        today = datetime.today()
        return render_template('index.html',
                               form_data_member=form_data_member,
                               today=today,
                               associados=associados,
                               pagamentos=pagamentos,
                               form_data_payment={})


def editar_associado():
    try:
        foto = processar_foto(request.files.get('foto', request.form.get('foto-atual', None)))
        associado = Associado(**request.form, foto=foto)
        sucesso, mensagem = Gateway.editar_associado(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit-member')
        associados = Gateway.listar_associados()
        pagamentos = Gateway.listar_pagamentos()
        today = datetime.today()
        return render_template('index.html',
                               form_data_member=form_data_member,
                               today=today,
                               associados=associados,
                               pagamentos=pagamentos,
                               form_data_payment={})


def remover_associado(cpf: CPF):
    try:
        sucesso, mensagem = Gateway.remover_associado(cpf)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o associado: {e}', 'danger-remove-member')
        return redirect(url_for('main.index'))
