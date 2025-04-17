from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Adocao, Gato, Usuario
from app import db
from app.decoradores import admin_required

adocoes = Blueprint("adocoes", __name__)

# Rota para adotar um gato
@adocoes.route("/adotar/<int:gato_id>", methods=['POST'])
@login_required
def adotar_gato(gato_id):
    gato = Gato.query.get_or_404(gato_id)
    
    novo_adocao = Adocao(usuario_id=current_user.id, gato_id=gato.id, status="Em análise")
    try:
        db.session.add(novo_adocao)
        db.session.commit()
        flash("Pedido de adoção realizado com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocorreu um erro: {e}", "error")

    return redirect(url_for('gatos.lista_gatos'))


# Listar adoções (admin)
@adocoes.route("/adocoes")
@admin_required
def listar_adocoes():
    query = Adocao.query.join(Gato).join(Usuario)

    status = request.args.get("status")
    if status:
        query = query.filter(Adocao.status.ilike(f"%{status}%"))

    nome_gato = request.args.get("nome_gato")
    if nome_gato:
        query = query.filter(Gato.nome.ilike(f"%{nome_gato}%"))

    nome_adotante = request.args.get("nome_adotante")
    if nome_adotante:
        query = query.filter(Usuario.nome.ilike(f"%{nome_adotante}%"))

    adocoes = query.all()
    return render_template("adocoes/adocoes.html", adocoes=adocoes)


# Listar adoções do usuário logado
@adocoes.route("/minhas-adocoes")
@login_required
def minhas_adocoes():
    adocoes = Adocao.query.filter_by(usuario_id=current_user.id).all()
    return render_template("adocoes/minhas_adocoes.html", adocoes=adocoes)


# Editar status de adoção (admin)
@adocoes.route("/adocao/<int:adocao_id>/editar", methods=["GET", "POST"])
@admin_required
def editar_adocao(adocao_id):
    adocao = Adocao.query.get_or_404(adocao_id)
    gato = adocao.gato

    if request.method == "POST":
        novo_status = request.form["status"]
        adocao.status = novo_status
        if novo_status == "Aceita":
            gato.status = "Adotado"
        elif novo_status == "Recusada":
            gato.status = "Disponível"
        db.session.commit()
        flash("Status da adoção atualizado!", "success")
        return redirect(url_for("adocoes.listar_adocoes"))

    return render_template("adocoes/editar_adocao.html", adocao=adocao)
