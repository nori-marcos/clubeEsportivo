import uuid
from datetime import datetime

from flask import request

from src.models.associado import Associado
from src.models.types import Titularidade, TipoPlano
from src.utils.arquivo_utils import processar_foto

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

def criar_associado_pelo_formulario(id_associado=None):
    id_associado = str(id_associado) if id_associado else uuid.uuid4().hex
    cpf = tratar_cpf(request.form['cpf'])
    nome = request.form['nome']
    data_nascimento = tratar_data(request.form['data_nascimento'])
    tipo = tratar_tipo(request.form['tipo'])
    endereco = request.form['endereco']
    telefone = tratar_telefone(request.form['telefone'])
    email = request.form['email']
    plano = tratar_plano(request.form['plano'])
    data_adesao = tratar_data(request.form['data_adesao'])

    foto = processar_foto(request.files['foto'])

    if foto is None:
        try:
            foto = request.form['foto-atual']
        except KeyError:
            foto = None

    return Associado(
        id_associado=id_associado,
        cpf=cpf,
        nome=nome,
        data_nascimento=data_nascimento,
        tipo=tipo,
        endereco=endereco,
        telefone=telefone,
        email=email,
        plano=plano,
        foto=foto,
        data_adesao=data_adesao
    )


def tratar_cpf(cpf) -> str:
    return cpf.replace('.', '').replace('-', '')


def tratar_telefone(telefone) -> str:
    return telefone.replace('(', '').replace(')', '').replace(' ', '').replace('-', '')


def tratar_tipo(tipo) -> Titularidade:
    try:
        return Titularidade[tipo.upper()]
    except KeyError:
        raise ValueError(f"Valor inválido para tipo: {tipo}")


def tratar_plano(plano) -> TipoPlano:
    try:
        return TipoPlano[plano.upper()]
    except KeyError:
        raise ValueError(f"Valor inválido para plano: {plano}")


def tratar_data(data_str) -> datetime.date:
    try:
        return datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        try:
            return datetime.strptime(data_str.split(' ')[0], '%Y-%m-%d').date()
        except ValueError:
            raise ValueError(f"Data inválida: {data_str}")
