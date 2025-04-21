from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_required
from app.models import Gato
from app import db
from app.decoradores import admin_required
from werkzeug.utils import secure_filename
import os

gatos = Blueprint('gatos', __name__)

@gatos.route('/gatos', methods=['GET'])
def lista_gatos():
    query = Gato.query

    nome = request.args.get('nome')
    if nome:
        query = query.filter(Gato.nome.ilike(f"%{nome}%"))

    idade = request.args.get('idade')
    if idade:
        query = query.filter(Gato.idade == int(idade))

    peso = request.args.get('peso')
    if peso:
        query = query.filter(Gato.peso == float(peso))

    status = request.args.get('status')
    if status:
        query = query.filter(Gato.status == status)

    gatos = query.all()
    return render_template('gatos/gatos.html', gatos=gatos)

@gatos.route('/gatos/novo', methods=['GET', 'POST'])
@admin_required  
def cadastrar_gato():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        peso = request.form['peso']
        chip = request.form['chip']
        status = request.form['status']
        imagem = request.files.get('imagem')

        nome_arquivo = None
        if imagem and imagem.filename != '':
            nome_arquivo = secure_filename(imagem.filename)
            caminho_imagem = os.path.join(current_app.static_folder, 'img', nome_arquivo)
            imagem.save(caminho_imagem)

        novo_gato = Gato(
            nome=nome,
            idade=idade,
            peso=peso,
            chip=chip,
            status=status,
            imagem=nome_arquivo
        )
        
        db.session.add(novo_gato)
        db.session.commit()
        return redirect(url_for('gatos.lista_gatos'))

    return render_template('gatos/formulario_gato.html')

@gatos.route('/gatos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_gato(id):
    gato = Gato.query.get_or_404(id)

    if request.method == 'POST':
        gato.nome = request.form['nome']
        gato.idade = request.form['idade']
        gato.peso = request.form['peso']
        gato.chip = request.form['chip']
        gato.status = request.form['status']
        gato.imagem = request.form.get('imagem', gato.imagem)

        imagem = request.files.get('imagem')
        if imagem and imagem.filename != '':
            filename = secure_filename(imagem.filename)
            caminho_upload = os.path.join(current_app.root_path, 'static', 'img', filename)
            imagem.save(caminho_upload)
            gato.imagem = filename  

        db.session.commit()
        return redirect(url_for('gatos.lista_gatos'))

    return render_template('gatos/editar_gato.html', gato=gato)

@gatos.route('/gatos/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_gato(id):
    gato = Gato.query.get_or_404(id)
    db.session.delete(gato)
    db.session.commit()
    return redirect(url_for('gatos.lista_gatos'))
