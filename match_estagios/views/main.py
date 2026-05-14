from flask import flash, redirect, request, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required

from match_estagios.extensions import db
from match_estagios.forms.basic_form import BasicForm
from match_estagios.models.candidatura import Candidatura, CandidaturaStatus
from match_estagios.models.user import UserRole, UserStatus
from match_estagios.models.vaga import Vaga, VagaStatus
from match_estagios.services.perfil_service import (
    choose_user_form,
    populate_form,
    save_form,
)
from match_estagios.utils.decorators import roles_required

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        mensagem = f"Logado como {current_user.email}"
    else:
        mensagem = "Não logado"
    return render_template("base.html", mensagem=mensagem)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.name}"


@main_bp.route("/perfil")
@login_required
def perfil():
    return render_template("main/perfil.html")


@main_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    try:
        form = choose_user_form(current_user)
    except ValueError:
        flash("Tipo de usuário inválido", "danger")
        return redirect(url_for("main.perfil"))

    print("pegou formulário")
    if request.method == "GET":
        populate_form(form, current_user)
        print("formulário populado")

    if form.validate_on_submit():
        print("formulário enviado")
        save_form(form, current_user)

        print("formulário salvo")
        flash("Perfil atualizado", "success")
        return redirect(url_for("main.perfil"))

    if form.errors:
        print(form.errors)

    return render_template("main/editar_perfil.html", form=form)


@main_bp.route("/vagas")
@login_required
def listar_vagas():
    vagas = Vaga.query.filter_by(status=VagaStatus.ABERTA).all()
    return render_template("main/vagas.html", vagas=vagas)


@main_bp.route("/vagas/<string:id>")
@login_required
def detalhes_vaga(id):
    form = BasicForm()
    vaga = Vaga.query.get_or_404(id)

    candidatura_existente = None

    if current_user.role == UserRole.ESTUDANTE and current_user.estudante:
        candidatura_existente = Candidatura.query.filter_by(
            id_estudante=current_user.estudante.id_estudante, id_vaga=vaga.id_vaga
        ).first()

    return render_template(
        "main/detalhes_vaga.html",
        form=form,
        vaga=vaga,
        candidatura_existente=candidatura_existente,
    )


@main_bp.route("/vagas/<string:id>/candidatar", methods=["POST"])
@login_required
@roles_required(UserRole.ESTUDANTE)
def candidatar(id):

    if current_user.status != UserStatus.VERIFICADO:
        flash("Sua conta precisa estar verificada", "danger")
        return redirect(url_for("main.detalhes_vaga", id=id))

    vaga = Vaga.query.get_or_404(id)

    candidatura_existente = Candidatura.query.filter_by(
        id_estudante=current_user.estudante.id_estudante,
        id_vaga=vaga.id_vaga,
    ).first()

    if candidatura_existente:
        flash("Você já se candidatou para esta vaga.", "warning")
        return redirect(url_for("main.detalhes_vaga", id=id))

    candidatura = Candidatura(
        id_estudante=current_user.estudante.id_estudante,
        id_vaga=vaga.id_vaga,
    )

    db.session.add(candidatura)
    db.session.commit()

    flash("Candidatura realizada com sucesso.", "success")

    return redirect(url_for("main.detalhes_vaga", id=id))


@main_bp.route("/minhas-candidaturas")
@login_required
@roles_required(UserRole.ESTUDANTE)
def minhas_candidaturas():

    form = BasicForm()

    candidaturas = Candidatura.query.filter_by(
        id_estudante=current_user.estudante.id_estudante
    ).all()

    return render_template(
        "main/minhas_candidaturas.html", form=form, candidaturas=candidaturas
    )


@main_bp.route(
    "/minhas-candidaturas/<string:id_candidatura>/cancelar", methods=["POST"]
)
@login_required
@roles_required(UserRole.ESTUDANTE)
def cancelar_candidatura(id_candidatura):

    candidatura = Candidatura.query.get_or_404(id_candidatura)

    if candidatura.id_estudante != current_user.estudante.id_estudante:
        flash("Sem permissão.", "danger")
        return redirect(url_for("main.minhas_candidaturas"))

    if candidatura.status != CandidaturaStatus.PENDENTE:
        flash("Você não pode cancelar essa candidatura.", "warning")
        return redirect(url_for("main.minhas_candidaturas"))

    db.session.delete(candidatura)
    db.session.commit()

    flash("Candidatura cancelada.", "success")

    return redirect(url_for("main.minhas_candidaturas"))
