from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario, Gato
from app import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app.decoradores import admin_required
import os

main = Blueprint('main', __name__)


@main.route("/")
def index():
   return render_template("index.html")

# Login
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redireciona para a página inicial se o usuário já estiver logado
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        # Autenticação do usuário
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for('main.login'))

    return render_template("login.html")

# Registro/criação de conta
@main.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Verificar se o email já está registrado
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("Este e-mail já está em uso. Por favor, escolha outro.", "error")
            return redirect(url_for('main.registro'))

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            # Redireciona para a página de login após o registro
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f"Erro ao salvar no banco: {str(e)}", "error")
            return redirect(url_for('main.registro'))

    return render_template("registro.html")

# Logout
@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for('main.index'))

@main.route("/admin/teste")
@admin_required
def admin_teste():
    return "Área de admin acessada com sucesso!"

# Lista de gatos 
@main.route('/gatos', methods=['GET'])
def lista_gatos():
    query = Gato.query

    # Aplicar filtros com base nos parâmetros da URL
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
    return render_template('gatos.html', gatos=gatos)

# Adicionar gato
@main.route('/gatos/novo', methods=['GET', 'POST'])
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
        return redirect(url_for('main.lista_gatos'))

    return render_template('formulario_gato.html')  # Formulário para criar gato



# Editar gato
@main.route('/gatos/<int:id>/editar', methods=['GET', 'POST'])
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
        return redirect(url_for('main.lista_gatos'))

    return render_template('editar_gato.html', gato=gato)

# Deletar gato
@main.route('/gatos/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_gato(id):
    gato = Gato.query.get_or_404(id) # Vai retornar um erro de 404 se o gato não existir na base
    db.session.delete(gato)
    db.session.commit()
    return redirect(url_for('main.lista_gatos'))
