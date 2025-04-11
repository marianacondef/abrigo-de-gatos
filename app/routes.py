from flask import Blueprint, render_template, request
from app.models import Usuario
from app import db
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)

# Página inicial
@main.route("/")
def index():
    return "<h1>Bem-vindo(a) ao Abrigo de Gatos! 🐱 </h1>"

# Login
@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        return f"Login tentado com: {email} / {senha}"
    
    return render_template("login.html")

# Registro
@main.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Cria o hash da senha antes de salvar
        senha_hash = generate_password_hash(senha)

        # Cria o usuário
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        # Salva no banco
        db.session.add(novo_usuario)
        db.session.commit()

        return f"Usuário {nome} registrado com sucesso!"

    return render_template("registro.html")
