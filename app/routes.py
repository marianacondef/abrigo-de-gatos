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

        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        try:
            db.session.add(novo_usuario)
            db.session.commit()
            return f"Usuário {nome} registrado com sucesso!"
        except Exception as e:
            return f"Erro ao salvar no banco: {str(e)}"

    return render_template("registro.html")