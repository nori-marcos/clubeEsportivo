from flask import request, flash, redirect, url_for, session

from gateway.associado_gateway import AssociadoGateway
from utils.formulario_utils import obter_dados_formulario_associado


def inserir_associado():
    try:
        associado = obter_dados_formulario_associado()
        sucesso, mensagem = AssociadoGateway.salvar(associado)
        return lidar_com_salvamento_associado(sucesso, mensagem)
    except Exception as e:
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger')
        return redirect(url_for('index'))


def editar_associado(id_associado):
    try:
        associado = obter_dados_formulario_associado(id_associado)
        sucesso, mensagem = AssociadoGateway.atualizar(associado)
        return lidar_com_salvamento_associado(sucesso, mensagem)
    except Exception as e:
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger')
        return redirect(url_for('index'))


def lidar_com_salvamento_associado(sucesso, mensagem):
    if sucesso:
        flash(mensagem, 'success')
        session.pop('form_data', None)
        return redirect('/')
    else:
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
        flash(mensagem, 'danger')
        return redirect(url_for('index'))
