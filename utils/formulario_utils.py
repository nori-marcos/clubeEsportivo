import uuid
from datetime import datetime

from flask import request

from models.associado import Associado
from utils.arquivo_utils import processar_foto


def obter_dados_formulario_associado(id_associado=None):
    cpf = request.form['cpf']
    nome = request.form['nome']
    data_nascimento = request.form['data_nascimento']
    tipo = request.form['tipo']
    endereco = request.form['endereco']
    telefone = request.form['telefone']
    email = request.form['email']
    plano = request.form['plano']
    foto = processar_foto(request.files.get('foto'))

    return Associado(
        id_associado=id_associado if id_associado else uuid.uuid4(),
        cpf=cpf,
        nome=nome,
        data_nascimento=data_nascimento,
        tipo=tipo,
        endereco=endereco,
        telefone=telefone,
        email=email,
        plano=plano,
        foto=foto,
        data_adesao=datetime.today()
    )
