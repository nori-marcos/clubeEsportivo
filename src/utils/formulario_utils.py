from datetime import datetime

from flask import request


def extrair_dados_formulario(id_associado=None):
    try:
        form_data = {
            'cpf': request.form['cpf'],
            'nome': request.form['nome'],
            'data_nascimento': request.form['data_nascimento'],
            'tipo': request.form['tipo'],
            'endereco': request.form['endereco'],
            'telefone': request.form['telefone'],
            'email': request.form['email'],
            'plano': request.form['plano'],
            'id_associado': id_associado
        }
        try:
            data_adesao = request.form['data_adesao']
            form_data['data_adesao'] = data_adesao
        except Exception as e:
            pass
        return form_data
    except Exception as e:
        return {}


def tratar_data(data_input) -> datetime.date:
    if isinstance(data_input, str):
        try:
            return datetime.strptime(data_input, '%Y-%m-%d').date()
        except ValueError:
            return datetime.strptime(data_input.split(' ')[0], '%Y-%m-%d').date()
    elif isinstance(data_input, datetime.date.__class__):
        return data_input
    else:
        raise