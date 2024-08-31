import base64
import uuid
from datetime import datetime

from flask import request, flash, redirect, url_for, session

from gateway.associado_gateway import AssociadoGateway
from models.associado import Associado


def inserir_associado():
    try:
        cpf = request.form['cpf']
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        tipo = request.form['tipo']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        email = request.form['email']
        plano = request.form['plano']

        foto = request.files.get('foto')

        if foto and allowed_file(foto.filename):
            foto_string = base64.b64encode(foto.read()).decode('utf-8')
        else:
            foto_string = None

        associado = Associado(
            id_associado=uuid.uuid4(),
            cpf=cpf,
            nome=nome,
            data_nascimento=data_nascimento,
            tipo=tipo,
            endereco=endereco,
            telefone=telefone,
            email=email,
            plano=plano,
            foto=foto_string,
            data_adesao=datetime.today()
        )

        sucesso, mensagem = AssociadoGateway.salvar(associado)

        if sucesso:
            flash(mensagem, 'success')
            session.pop('form_data', None)
            return redirect('/')
        else:
            session['form_data'] = {
                'cpf': cpf,
                'nome': nome,
                'data_nascimento': data_nascimento,
                'tipo': tipo,
                'endereco': endereco,
                'telefone': telefone,
                'email': email,
                'plano': plano
            }
            flash(mensagem, 'danger')

    except Exception as e:
        flash(f'Ocorreu um erro ao adicionar o associado: {e}', 'danger')

    return redirect(url_for('index'))


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
