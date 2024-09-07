import base64
from io import BytesIO

from PIL import Image


def processar_foto(foto) -> str | None:
    if foto and arquivo_permitido(foto.filename):
        return base64.b64encode(foto.read()).decode('utf-8')
    return None


def arquivo_permitido(nome_arquivo) -> bool:
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in extensoes_permitidas


def validar_foto_base64(foto_base64) -> bool:
    try:
        if foto_base64.startswith('data:image'):
            foto_base64 = foto_base64.split(',')[1]

        image_data = base64.b64decode(foto_base64)
        image = Image.open(BytesIO(image_data))

        if image.format.lower() not in {'png', 'jpg', 'jpeg', 'gif'}:
            return False

        image.verify()
        return True
    except Exception as e:
        print(f"Erro ao validar a imagem: {e}")
        return False
