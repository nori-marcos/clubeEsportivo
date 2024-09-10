from datetime import datetime, date

from flask import flash, redirect, url_for, render_template

from src.gateway.pagamento_gateway import Pagamento_Gateway
from src.models.pagamento import Pagamento

pagamentos_mock = [
    {
        'contrato': '2',
        'data_vencimento': '2021-10-10',
        'data_pagamento': '2021-10-10',
        'valor': 100.0,
    },
    {
        'contrato': '1',
        'data_vencimento': '2021-10-10',
        'data_pagamento': '2021-10-10',
        'valor': 100.0,
    }
]

def listar_pagamento(cpf, data):
    pagamentos: list[Pagamento] = [Pagamento(**dado) for dado in Pagamento_Gateway.listar_pagamentos(cpf)]
    return pagamentos

def inserir_pagamento():
    try:
        sucesso, mensagem = True, "Pagamento adicionado com sucesso"
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = {}
        flash(f'Ocorreu um erro ao adicionar o pagamento: {e}', 'danger-insert-payment')
        associados = Pagamento_Gateway.listar_associados()
        # pagamentos = Pagamento_Gateway.listar_pagamentos()

        pagamentos = pagamentos_mock

        today = datetime.today()
        return render_template('index.html',
                               form_data_member=form_data_member,
                               today=today,
                               associados=associados,
                               pagamentos=pagamentos,
                               form_data_payment={})


def editar_pagamento(cpf, data: date):
    pagamento = listar_pagamento(cpf, data)[0]

    try:
        sucesso, mensagem = Pagamento_Gateway.editar_pagamento(pagamento)
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        form_data_member = {}
        flash(f'Ocorreu um erro ao atualizar o pagamento: {e}', 'danger-edit-payment')
        associados = Pagamento_Gateway.listar_associados()
        # pagamentos = Pagamento_Gateway.listar_pagamentos()
        pagamentos = pagamentos_mock


        today = datetime.today()
        return render_template('index.html',
                               form_data_member=form_data_member,
                               today=today,
                               associados=associados,
                               pagamentos=pagamentos,
                               form_data_payment={})


def remover_pagamento(pagamento:):
    try:
        sucesso, mensagem = True, "Pagamento removido com sucesso"
        if sucesso:
            flash(mensagem, 'success')
            return redirect(url_for('main.index'))
    except Exception as e:
        flash(f'Ocorreu um erro ao remover o pagamento: {e}', 'danger-remove-payment')
        return redirect(url_for('main.index'))
