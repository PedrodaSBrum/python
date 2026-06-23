from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Filme, Ingresso, Sala, Sessao, db

cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")


@cinema_bp.route("/")
def index():
    sessoes = Sessao.listar_com_detalhes()
    return render_template("cinema/lista_sessoes.html", sessoes=sessoes)


@cinema_bp.route("/sessao/cadastrar", methods=["GET", "POST"])
def cadastrar_sessao():
    filmes = Filme.listar()
    salas = Sala.listar()

    if request.method == "POST":
        filme_id = request.form.get("filme_id")
        sala_id = request.form.get("sala_id")
        data_hora_str = request.form.get("data_hora")
        preco = request.form.get("preco")

        try:
            data_hora = datetime.strptime(data_hora_str, "%Y-%m-%dT%H:%M")
            nova_sessao = Sessao(
                filme_id=int(filme_id),
                sala_id=int(sala_id),
                data_hora=data_hora,
                preco=float(preco),
            )
            db.session.add(nova_sessao)
            db.session.commit()
            flash("Sessão cadastrada com sucesso!", "sucesso")
            return redirect(url_for("cinema.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao cadastrar sessão: {e}", "erro")

    return render_template(
        "cinema/formulario_sessao.html",
        filmes=filmes,
        salas=salas,
    )


@cinema_bp.route("/sessao/<int:sessao_id>/excluir", methods=["POST"])
def excluir_sessao(sessao_id):
    sessao = Sessao.query.get_or_404(sessao_id)
    db.session.delete(sessao)
    db.session.commit()
    flash("Sessão removida.", "sucesso")
    return redirect(url_for("cinema.index"))


# ── Ponto extra: compra de ingresso ──────────────────────────────────────────

@cinema_bp.route("/sessao/<int:sessao_id>/ingresso", methods=["GET", "POST"])
def comprar_ingresso(sessao_id):
    sessao = Sessao.query.get_or_404(sessao_id)

    if request.method == "POST":
        assento = request.form.get("assento", "").strip().upper()
        nome = request.form.get("nome_comprador", "").strip()

        if assento in sessao.assentos_ocupados():
            flash(f"Assento {assento} já está ocupado. Escolha outro.", "erro")
        elif sessao.vagas_disponiveis() <= 0:
            flash("Sessão lotada!", "erro")
        else:
            ingresso = Ingresso(sessao_id=sessao_id, assento=assento, nome_comprador=nome)
            db.session.add(ingresso)
            db.session.commit()
            flash(f"Ingresso comprado! Assento {assento} confirmado.", "sucesso")
            return redirect(url_for("cinema.index"))

    return render_template("cinema/comprar_ingresso.html", sessao=sessao)
