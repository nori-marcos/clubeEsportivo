import base64

from flask import request


def processar_foto(foto) -> bytes | None:
    if foto and arquivo_permitido(foto.filename):
        return base64.b64encode(foto.read())
    return request.form.get('foto-atual')


def arquivo_permitido(nome_arquivo) -> bool:
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in extensoes_permitidas
