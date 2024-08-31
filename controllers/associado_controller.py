from flask import request, redirect, url_for

from models.associado import Associado


def inserir_associado():
    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        plano = request.form['plano']

        novo_associado = Associado(cpf=cpf, nome=nome, email=email, telefone=telefone, plano=plano)

        try:
            novo_associado.save()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {e}"
