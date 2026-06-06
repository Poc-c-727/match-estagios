from flask import flash, redirect, request, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required

from match_estagios.extensions import db
from match_estagios.forms.basic_form import BasicForm
from match_estagios.forms.verificacao import SolicitacaoVerificacaoForm
from match_estagios.models.candidatura import Candidatura, CandidaturaStatus
from match_estagios.models.faculdade import Faculdade
from match_estagios.models.notificacao import Notificacao
from match_estagios.models.user import UserRole, UserStatus
from match_estagios.models.vaga import Vaga, VagaStatus
from match_estagios.models.verificacao import SolicitacaoStatus, SolicitacaoVerificacao
from match_estagios.services.perfil_service import (
    choose_user_form,
    populate_form,
    save_form,
)
from match_estagios.utils.decorators import roles_required

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def index():
    # if current_user.is_authenticated:
    #     return render_template("index_logged.html")
    # Talve não seja necessário um "index_logged", um "redirecionador" para uma
    # tela adequada para cada usuário. Criei um arquivo `templates/index_logged.html`
    # para evitar que o código quebre se o código for descomentado.
    return render_template("index.html")


@main_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


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

    if form.validate_on_submit():
        save_form(form, current_user)

        flash("Perfil atualizado", "success")
        return redirect(url_for("main.perfil"))

    if form.errors:
        print(form.errors)

    return render_template("main/editar_perfil.html", form=form)


@main_bp.route("/perfil/verificacao", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.ESTUDANTE)
def solicitar_verificacao():

    if current_user.status != UserStatus.PENDENTE:
        flash("Sua conta já foi verificada.", "warning")
        return redirect(url_for("main.perfil"))

    form = SolicitacaoVerificacaoForm()

    faculdades = Faculdade.query.all()

    form.id_faculdade.choices = [
        (faculdade.id_faculdade, faculdade.name) for faculdade in faculdades
    ]

    if form.validate_on_submit():
        solicitacao_existente = SolicitacaoVerificacao.query.filter_by(
            id_user=current_user.id_user, status=SolicitacaoStatus.PENDENTE
        ).first()

        if solicitacao_existente:
            flash("Você já possui uma solicitação pendente.", "warning")
            return redirect(url_for("main.perfil"))

        print("solicitação enviada")
        solicitacao = SolicitacaoVerificacao(
            ra=form.ra.data,
            cpf=form.cpf.data,
            curso=form.curso.data,
            data_nascimento=form.data_nascimento.data,
            endereco=form.endereco.data,
            telefone=form.telefone.data,
            id_faculdade=form.id_faculdade.data,
            id_user=current_user.id_user,
        )
        print("instância da solicitação criada")

        db.session.add(solicitacao)
        db.session.commit()
        print("solicitação adicionada")

        flash("Solicitação enviada com sucesso.", "success")
        return redirect(url_for("main.perfil"))

    return render_template("main/solicitar_verificacao.html", form=form)


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


@main_bp.route("/notificacoes")
@login_required
def notificacoes():
    form = BasicForm()
    notificacoes_nao_lidas = (
        Notificacao.query.filter_by(id_user=current_user.id_user, lida=False)
        .order_by(Notificacao.data_criacao.desc())
        .all()
    )

    notificacoes_lidas = (
        Notificacao.query.filter_by(id_user=current_user.id_user, lida=True)
        .order_by(Notificacao.data_criacao.desc())
        .all()
    )

    return render_template(
        "main/notificacoes.html",
        form=form,
        notificacoes_nao_lidas=notificacoes_nao_lidas,
        notificacoes_lidas=notificacoes_lidas,
    )


@main_bp.route("/notificacoes/<string:id_notificacao>/ler", methods=["POST"])
@login_required
def marcar_notificacao_lida(id_notificacao):
    notificacao = Notificacao.query.get_or_404(id_notificacao)

    if notificacao.id_user != current_user.id_user:
        flash("Sem permissão.", "danger")
        return redirect(url_for("main.notificacoes"))

    notificacao.lida = True

    db.session.commit()

    return redirect(url_for("main.notificacoes"))


@main_bp.route("/notificacoes/marcar-todas", methods=["POST"])
@login_required
def marcar_notificacoes_lida():
    notificacoes = Notificacao.query.filter_by(
        id_user=current_user.id_user,
        lida=False,
    ).all()

    for notificacao in notificacoes:
        notificacao.lida = True

    db.session.commit()

    flash("Todas as notificações foram marcadas como lidas.", "success")

    return redirect(url_for("main.notificacoes"))
