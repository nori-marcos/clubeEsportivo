from typing import List

from flask import request

from src.models.types import CPF, Telefone


def extrair_dados_formulario():
    form_data_member = {}
    if 'data_adesao' in request.form:
        form_data_member['data_adesao'] = request.form['data_adesao']
    campos = ['cpf', 'nome', 'data_nascimento', 'tipo', 'endereco', 'telefone', 'email', 'plano']
    for campo in campos:
        campo_valor = extrair_campos_formulario(campo)
        if campo_valor is not None:
            form_data_member[campo] = campo_valor
    return form_data_member


def extrair_campos_formulario(campo: str):
    return request.form.get(campo, '')


def extrair_telefones(cpf: CPF) -> List[Telefone]:
    telefones = []

    telefone1_form = request.form.get('telefone1', None)
    if telefone1_form:
        telefone1 = Telefone(dono=cpf, telefone=telefone1_form)
        telefones.append(telefone1)

    telefone2_form = request.form.get('telefone2', None)
    if telefone2_form:
        telefone2 = Telefone(dono=cpf, telefone=telefone2_form)
        telefones.append(telefone2)

    return telefones
