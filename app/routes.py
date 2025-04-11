from flask import Blueprint, render_template, request

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
        senha = request.form['senha']  # Aqui acessa a senha corretamente
        return f"Conta criada para: {nome} ({email}) com senha: {senha}"
    
    return render_template("registro.html")