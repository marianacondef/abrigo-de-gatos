from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from app.models import Usuario
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.decoradores import admin_required

main = Blueprint('main', __name__)


@main.route("/")
def index():
    """Rota principal, exibe a página inicial.

    Returns:
        str: Template da página inicial (`index.html`).
    """
    return render_template("index.html")


@main.route("/login", methods=['GET', 'POST'])
def login():
    """Rota para login de usuário.

    Se o usuário já estiver logado, ele será redirecionado para a página inicial.
    Caso contrário, valida as credenciais enviadas no formulário de login.

    POST:
        Args:
            email (str): E-mail do usuário.
            senha (str): Senha do usuário.

    Returns:
        str: Template da página de login (`login.html`) ou redirecionamento para
        a página inicial em caso de sucesso.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main.index'))
        else:
            flash("Email ou senha inválidos.", "error")
            return redirect(url_for('main.login'))

    return render_template("login.html")


@main.route("/registro", methods=['GET', 'POST'])
def registro():
    """Rota para registro de novos usuários.

    Cria um novo usuário com os dados fornecidos no formulário. Antes do registro,
    verifica se o e-mail já está em uso.

    POST:
        Args:
            nome (str): Nome do usuário.
            email (str): E-mail do usuário.
            senha (str): Senha do usuário.

    Returns:
        str: Template da página de registro (`registro.html`) ou redirecionamento
        para a página de login em caso de sucesso.
    """
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash("Este e-mail já está em uso. Por favor, escolha outro.", "error")
            return redirect(url_for('main.registro'))

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for('main.login'))
        except Exception as e:
            flash(f"Erro ao salvar no banco: {str(e)}", "error")
            return redirect(url_for('main.registro'))

    return render_template("registro.html")


@main.route("/logout")
@login_required
def logout():
    """Rota para logout do sistema.

    Apenas usuários autenticados podem acessar essa rota.
    Redireciona para a página inicial após o logout.

    Returns:
        str: Redirecionamento para a página inicial (`index.html`).
    """
    logout_user()
    flash("Você foi desconectado com sucesso.", "success")
    return redirect(url_for('main.index'))


@main.route("/admin/teste")
@admin_required
def admin_teste():
    """Rota de exemplo para verificar o acesso de administradores.

    Essa rota só pode ser acessada por usuários com permissão de administrador.

    Returns:
        str: Mensagem indicando que a área de admin foi acessada com sucesso.
    """
    return "Área de admin acessada com sucesso!"