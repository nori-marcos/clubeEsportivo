from flask import request, flash, redirect, url_for, session

from gateway.associado_gateway import AssociadoGateway
from utils.formulario_utils import obter_dados_formulario_associado


def inserir_associado():
    try:
        associado = obter_dados_formulario_associado()
        sucesso, mensagem = AssociadoGateway.salvar(associado)
        if sucesso:
            flash(mensagem, 'success')
            session.pop('form_data', None)
            return redirect('/')
        else:
            flash(mensagem, 'danger-insert')
            return redirect(url_for('index'))
    except Exception as e:
        session['form_data'] = {
            'cpf': request.form['cpf'],
            'nome': request.form['nome'],
            'data_nascimento': request.form['data_nascimento'],
            'tipo': request.form['tipo'],
            'endereco': request.form['endereco'],
            'telefone': request.form['telefone'],
            'email': request.form['email'],
            'plano': request.form['plano']
        }
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert')
        return redirect(url_for('index'))


def editar_associado(id_associado):
    try:
        associado = obter_dados_formulario_associado(id_associado)
        sucesso, mensagem = AssociadoGateway.editar(associado)
        if sucesso:
            flash(mensagem, 'success')
            session.pop('form_data', None)
            return redirect('/')
        else:
            flash(mensagem, 'danger-edit')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit')
        return redirect(url_for('index'))


def remover_associado(id_associado):
    sucesso, mensagem = AssociadoGateway.remover(id_associado)
    if sucesso:
        flash(mensagem, 'success')
    else:
        flash(mensagem, 'danger-remove')
    return redirect(url_for('index'))
