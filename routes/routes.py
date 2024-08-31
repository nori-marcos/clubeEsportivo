from flask import render_template, session

from app import app
from controllers import associado_controller


@app.route('/')
def index():
    form_data = session.pop('form_data', {})
    return render_template('index.html', form_data=form_data)


@app.route('/inserir/associado', methods=['POST'])
def inserir_associado():
    return associado_controller.inserir_associado()
