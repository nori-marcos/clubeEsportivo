from datetime import datetime

from flask import flash, redirect, url_for, render_template

from src.gateway.gateway import Gateway


def listar_pagamentos():
    return Gateway.listar_pagamentos()


def inserir_pagamento():
    try:
        sucesso, mensagem = True, "Pagamento adicionado com sucesso"
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = {}
        flash(f'Ocorreu um erro ao adicionar o pagamento: {e}', 'danger-insert-payment')
        associados = Gateway.listar_associados()
        # pagamentos = Gateway.listar_pagamentos()

        # mock
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


def editar_pagamento():
    try:
        sucesso, mensagem = True, "Pagamento atualizado com sucesso"
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = {}
        flash(f'Ocorreu um erro ao atualizar o pagamento: {e}', 'danger-edit-payment')
        associados = Gateway.listar_associados()
        # pagamentos = Gateway.listar_pagamentos()

        # mock
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


def remover_pagamento(id_pagamento):
    try:
        sucesso, mensagem = True, "Pagamento removido com sucesso"
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o pagamento: {e}', 'danger-remove-payment')
        return redirect(url_for('main.index'))
