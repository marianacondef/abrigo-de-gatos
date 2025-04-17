from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Medicacao, Gato
from app import db
from app.decoradores import admin_required

medicacoes = Blueprint("medicacoes", __name__)

# Listar medicações (admin)
@medicacoes.route("/medicacoes")
@admin_required
def listar_medicacoes():
    medicacoes = Medicacao.query.all()
    return render_template("medicacoes/listar.html", medicacoes=medicacoes)

# Adicionar medicação
@medicacoes.route("/medicacoes/nova", methods=["GET", "POST"])
@admin_required
def nova_medicacao():
    gatos = Gato.query.all()

    if request.method == "POST":
        nome = request.form["nome"]
        dosagem = request.form["dosagem"]
        frequencia = request.form["frequencia"]
        data_inicio = request.form["data_inicio"]
        data_fim = request.form.get("data_fim")
        gato_id = request.form["gato_id"]

        nova_medicacao = Medicacao(
            nome=nome,
            dosagem=dosagem,
            frequencia=frequencia,
            data_inicio=data_inicio,
            data_fim=data_fim if data_fim else None,
            gato_id=gato_id
        )

        db.session.add(nova_medicacao)
        db.session.commit()
        flash("Medicação adicionada com sucesso!", "success")
        return redirect(url_for("medicacoes.listar_medicacoes"))
    
    return render_template("medicacoes/nova.html", gatos=gatos)

# Editar medicação
@medicacoes.route("/medicacoes/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def editar_medicacao(id):
    medicacao = Medicacao.query.get_or_404(id)
    gatos = Gato.query.all()

    if request.method == "POST":
        medicacao.nome = request.form["nome"]
        medicacao.dosagem = request.form["dosagem"]
        medicacao.frequencia = request.form["frequencia"]
        medicacao.data_inicio = request.form["data_inicio"]
        medicacao.data_fim = request.form.get("data_fim")
        medicacao.gato_id = request.form["gato_id"]

        db.session.commit()
        flash("Medicação atualizada com sucesso!", "success")
        return redirect(url_for("medicacoes.listar_medicacoes"))
    
    return render_template("medicacoes/editar.html", medicacao=medicacao, gatos=gatos)

# Deletar medicação
@medicacoes.route("/medicacoes/<int:id>/deletar", methods=["POST"])
@admin_required
def deletar_medicacao(id):
    medicacao = Medicacao.query.get_or_404(id)
    db.session.delete(medicacao)
    db.session.commit()
    flash("Medicação deletada com sucesso!", "success")
    return redirect(url_for("medicacoes.listar_medicacoes"))
