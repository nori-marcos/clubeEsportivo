from datetime import datetime

from flask import request

from src.models.associado import Associado
from src.utils.arquivo_utils import processar_foto


def extrair_dados_formulario():
    form_data = {}
    if 'data_adesao' in request.form:
        form_data['data_adesao'] = request.form['data_adesao']
    campos = ['cpf', 'nome', 'data_nascimento', 'tipo', 'endereco', 'telefone', 'email', 'plano']
    for campo in campos:
        campo_valor = extrair_campos_formulario(campo)
        if campo_valor is not None:
            form_data[campo] = campo_valor
    return form_data


def extrair_campos_formulario(campo: str):
    return request.form.get(campo, '')


def criar_associado_pelo_formulario():
    try:
        cpf = request.form.get('cpf', '')
        nome = request.form.get('nome', '')
        data_nascimento = request.form.get('data_nascimento', '')
        tipo = request.form.get('tipo', '')
        endereco = request.form.get('endereco', '')
        telefone = request.form.get('telefone', '')
        email = request.form.get('email', '')
        plano = request.form.get('plano', '')
        data_adesao = request.form.get('data_adesao', datetime.today().strftime('%Y-%m-%d'))

        foto = processar_foto(request.files.get('foto', None))

        if foto is None:
            foto = request.form.get('foto-atual', None)

        return Associado(
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento,
            tipo=tipo,
            endereco=endereco,
            telefone=telefone,
            email=email,
            plano=plano,
            foto=foto,
            data_adesao=data_adesao)

    except KeyError as e:
        raise ValueError(f"Campo obrigatório ausente: {e}")
    except ValueError as e:
        raise ValueError(f"Erro de validação: {e}")
    except Exception as e:
        raise RuntimeError(f"Erro ao criar associado: {e}")
