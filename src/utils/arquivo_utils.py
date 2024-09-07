import base64
from io import BytesIO

from PIL import Image
from flask import request


def processar_foto(foto) -> str | None:
    if foto and arquivo_permitido(foto.filename):
        return base64.b64encode(foto.read()).decode('utf-8')
    return request.form.get('foto-atual')


def arquivo_permitido(nome_arquivo) -> bool:
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in extensoes_permitidas


def validar_foto_base64(foto) -> bool | None:
    try:
        image_data = base64.b64decode(foto)
        image = Image.open(BytesIO(image_data))
        image.verify()  # Verifica se é uma imagem válida
        return True
    except Exception as e:
        return False
