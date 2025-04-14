from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario, Gato
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.decoradores import admin_required

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
@main.route("/gatos")
def lista_gatos():
    gatos = Gato.query.all()
    return render_template("gatos.html", gatos=gatos)