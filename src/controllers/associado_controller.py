from datetime import datetime

from flask import flash, render_template, redirect, url_for, request

from src.gateway.gateway import Gateway
from src.models.associado import Associado
from src.models.types import CPF
from src.utils.arquivo_utils import processar_foto
from src.utils.formulario_utils import extrair_dados_formulario, extrair_telefones


def listar_associados():
    return Gateway.listar_associados()


def inserir_associado():
    try:
        foto = processar_foto(request.files.get('foto', None))

        cpf = CPF(cpf=request.form.get('cpf'))
        telefones = extrair_telefones(cpf)

        associado = Associado(
            cpf=cpf,
            nome=request.form.get('nome'),
            email=request.form.get('email'),
            tipo=request.form.get('tipo'),
            plano=request.form.get('plano'),
            data_nascimento=request.form.get('data_nascimento'),
            endereco=request.form.get('endereco'),
            foto=foto,
            telefones=telefones,
            associado_titular=request.form.get('associado_titular', None),
        )

        sucesso, mensagem = Gateway.salvar_associado(associado)

        if sucesso:
            flash(mensagem, 'success')
        return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger-insert-member')
        associados = Gateway.listar_associados()
        pagamentos = [
            {
                'id_pagamento': 1,
                'cpf_associado': '123.456.789-00',
                'nome_associado': 'Fulano de Tal',
                'data_vencimento': '2021-10-10',
                'data_pagamento': '2021-10-10',
                'valor': 100.0,
                'tipo': 'Mensalidade',
                'metodo': 'Pix',
                'descricao': 'Pagamento da mensalidade de outubro'
            },
            {
                'id_pagamento': 2,
                'cpf_associado': '123.456.789-00',
                'nome_associado': 'Fulano de Tal',
                'data_vencimento': '2021-10-10',
                'data_pagamento': '2021-10-10',
                'valor': 100.0,
                'tipo': 'Mensalidade',
                'metodo': 'Pix',
                'descricao': 'Pagamento da mensalidade de outubro'
            }
        ]
        today = datetime.today()
        return render_template('index.html',
                               form_data_member=form_data_member,
                               today=today,
                               associados=associados,
                               pagamentos=pagamentos,
                               form_data_payment={})


def editar_associado():
    try:
        foto_final = None

        foto_associado = request.form.get('foto_atual')
        foto_nova = processar_foto(request.files.get('foto', None))

        if foto_nova:
            foto_final = foto_nova
        elif foto_associado:
            foto_final = foto_associado

        cpf = CPF(cpf=request.form.get('cpf'))
        telefones = extrair_telefones(cpf)

        associado = Associado(
            cpf=cpf,
            nome=request.form.get('nome'),
            email=request.form.get('email'),
            tipo=request.form.get('tipo'),
            plano=request.form.get('plano'),
            data_nascimento=request.form.get('data_nascimento'),
            endereco=request.form.get('endereco'),
            foto=foto_final,
            telefones=telefones,
            data_adesao=request.form.get('data_adesao'),
            associado_titular=request.form.get('associado_titular', None),
        )

        sucesso, mensagem = Gateway.editar_associado(associado)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = extrair_dados_formulario()
        flash(f'Ocorreu um erro ao atualizar o associado: {e}', 'danger-edit-member')
        associados = Gateway.listar_associados()
        pagamentos = [
            {
                'id_pagamento': 1,
                'cpf_associado': '123.456.789-00',
                'nome_associado': 'Fulano de Tal',
                'data_vencimento': '2021-10-10',
                'data_pagamento': '2021-10-10',
                'valor': 100.0,
                'tipo': 'Mensalidade',
                'metodo': 'Pix',
                'descricao': 'Pagamento da mensalidade de outubro'
            },
            {
                'id_pagamento': 2,
                'cpf_associado': '123.456.789-00',
                'nome_associado': 'Fulano de Tal',
                'data_vencimento': '2021-10-10',
                'data_pagamento': '2021-10-10',
                'valor': 100.0,
                'tipo': 'Mensalidade',
                'metodo': 'Pix',
                'descricao': 'Pagamento da mensalidade de outubro'
            }
        ]
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
