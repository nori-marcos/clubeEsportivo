from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from src.controllers import associado_controller, pagamento_controller
from src.main import bp


@bp.route('/')
def index():
    associados = associado_controller.listar_associados()
    # pagamentos = pagamento_controller.listar_pagamentos()
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
                           associados=associados,
                           pagamentos=pagamentos,
                           today=today,
                           form_data_member={},
                           form_data_payment={})


@bp.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()


@bp.route('/editar/associado', methods=['POST'])
def editar_associado():
    return associado_controller.editar_associado()


@bp.route('/remover_associado/<cpf_associado>', methods=['GET', 'POST'])
def remover_associado(cpf_associado):
    if request.form.get('_method') == 'DELETE':
        return associado_controller.remover_associado(cpf_associado)
    flash('Método não permitido', 'danger')
    return redirect(url_for('main.index'))


@bp.route('/inserir/pagamento', methods=['POST'])
def inserir_pagamento():
    return pagamento_controller.inserir_pagamento()


@bp.route('/remover_pagamento/<id_pagamento>', methods=['GET', 'POST'])
def remover_pagamento(id_pagamento):
    if request.form.get('_method') == 'DELETE':
        return pagamento_controller.remover_pagamento(id_pagamento)
    flash('Método não permitido', 'danger')
    return redirect(url_for('main.index'))
