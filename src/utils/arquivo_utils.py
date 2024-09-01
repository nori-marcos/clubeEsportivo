import base64


def processar_foto(foto):
    if foto and arquivo_permitido(foto.filename):
        return base64.b64encode(foto.read()).decode('utf-8')
    return None


def arquivo_permitido(nome_arquivo):
    extensoes_permitidas = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in extensoes_permitidas
