from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

# Página inicial
@main.route("/")
def index():
    return "<h1>Bem-vindo(a) ao Abrigo de Gatos! 🐱 </h1>"

# Login
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redireciona para a página inicial se o usuário já estiver logado

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.query.filter_by(email=email).first()

        # Autenticação do usuário
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main.index'))  # Redireciona para a página inicial após o login
        else:
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for('main.login'))

    return render_template("login.html")

# Registro
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
            return redirect(url_for('main.login'))  # Redireciona para a página de login após o registro
        except Exception as e:
            flash(f"Erro ao salvar no banco: {str(e)}", "error")
            return redirect(url_for('main.registro'))

    return render_template("registro.html")

# Logout
@main.route("/logout")
@login_required  # Só pode acessar se estiver logado
def logout():
    logout_user()  # Desconecta o usuário
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for('main.index'))  # Redireciona para a página inicial após o logout
