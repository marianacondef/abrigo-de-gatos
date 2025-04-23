from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Medicacao, Gato
from app import db
from app.decoradores import admin_required

medicacoes = Blueprint("medicacoes", __name__)


@medicacoes.route("/medicacoes")
@admin_required
def listar_medicacoes():
    """Lista todas as medicações cadastradas no sistema.

    Apenas administradores têm acesso a esta rota.

    Returns:
        str: Template da página (`medicacoes/listar.html`), com as medicações listadas.
    """
    medicacoes = Medicacao.query.all()
    return render_template("medicacoes/listar.html", medicacoes=medicacoes)


@medicacoes.route("/medicacoes/nova", methods=["GET", "POST"])
@admin_required
def nova_medicacao():
    """Adiciona uma nova medicação ao sistema.

    Apenas administradores têm acesso a esta rota. No metodo GET, exibe
    o formulário para cadastrar a medicação. No metodo POST, processa os dados
    do formulário e salva a medicação no banco de dados.

    POST:
        Args:
            nome (str): Nome da medicação.
            dosagem (str): Dosagem da medicação.
            frequencia (str): Frequência da aplicação.
            data_inicio (str): Data de início.
            data_fim (str, opcional): Data de término.
            gato_id (int): ID do gato que receberá a medicação.

    Returns:
        str: Redirecionamento para a lista de medicações ou o template do formulário.
    """
    gatos = Gato.query.all()

    if request.method == "POST":
        nome = request.form.get("nome")
        dosagem = request.form.get("dosagem")
        frequencia = request.form.get("frequencia")
        data_inicio = request.form.get("data_inicio")
        data_fim = request.form.get("data_fim")
        gato_id = request.form.get("gato_id")

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


@medicacoes.route("/medicacoes/<int:id>/editar", methods=["GET", "POST"])
@admin_required
def editar_medicacao(id):
    """Edita as informações de uma medicação existente.

    Apenas administradores têm acesso a esta rota. No metodo GET, exibe
    o formulário para edição. No metodo POST, processa os dados e atualiza
    a medicação no banco de dados.

    Args:
        id (int): ID da medicação a ser editada.

    Returns:
        str: Redirecionamento para a lista de medicações ou o template do formulário.
    """
    medicacao = Medicacao.query.get_or_404(id)
    gatos = Gato.query.all()

    if request.method == "POST":
        medicacao.nome = request.form.get("nome")
        medicacao.dosagem = request.form.get("dosagem")
        medicacao.frequencia = request.form.get("frequencia")
        medicacao.data_inicio = request.form.get("data_inicio")
        medicacao.data_fim = request.form.get("data_fim")
        medicacao.gato_id = request.form.get("gato_id")

        db.session.commit()
        flash("Medicação atualizada com sucesso!", "success")
        return redirect(url_for("medicacoes.listar_medicacoes"))

    return render_template("medicacoes/editar.html", medicacao=medicacao, gatos=gatos)


@medicacoes.route("/medicacoes/<int:id>/deletar", methods=["POST"])
@admin_required
def deletar_medicacao(id):
    """Exclui uma medicação do sistema.

    Apenas administradores têm acesso a esta rota.

    Args:
        id (int): ID da medicação a ser deletada.

    Returns:
        str: Redirecionamento para a lista de medicações.
    """
    medicacao = Medicacao.query.get_or_404(id)
    db.session.delete(medicacao)
    db.session.commit()
    flash("Medicação deletada com sucesso!", "success")
    return redirect(url_for("medicacoes.listar_medicacoes"))