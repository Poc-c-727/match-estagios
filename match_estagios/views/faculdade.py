from flask import flash, redirect, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required

from match_estagios.extensions import db
from match_estagios.forms.basic_form import BasicForm
from match_estagios.models.estudante import Estudante
from match_estagios.models.user import UserRole, UserStatus
from match_estagios.models.verificacao import SolicitacaoStatus, SolicitacaoVerificacao
from match_estagios.utils.decorators import roles_required

faculdade_bp = Blueprint("faculdade", __name__, template_folder=("templates"))


@faculdade_bp.route("/verificacoes")
@login_required
@roles_required(UserRole.FACULDADE)
def listar_verificacoes():
    solicitacoes = SolicitacaoVerificacao.query.filter_by(
        id_faculdade=current_user.faculdade.id_faculdade,
        status=SolicitacaoStatus.PENDENTE,
    ).all()

    return render_template(
        "faculdade/verificacoes/listar.html",
        solicitacoes=solicitacoes,
    )


@faculdade_bp.route("/verificacoes/<string:id_solicitacao>")
@login_required
@roles_required(UserRole.FACULDADE)
def detalhes_verificacao(id_solicitacao):
    form = BasicForm()
    solicitacao = SolicitacaoVerificacao.query.get_or_404(id_solicitacao)

    if solicitacao.id_faculdade != current_user.faculdade.id_faculdade:
        flash("Sem permissão.", "danger")
        return redirect(url_for("Faculdade.listar_verificacoes"))

    return render_template(
        "faculdade/verificacoes/detalhes.html",
        form=form,
        solicitacao=solicitacao,
    )


@faculdade_bp.route("/verificacoes/<string:id_solicitacao>/aprovar", methods=["POST"])
@login_required
@roles_required(UserRole.FACULDADE)
def aprovar_verificacao(id_solicitacao):
    solicitacao = SolicitacaoVerificacao.query.get_or_404(id_solicitacao)

    if solicitacao.id_faculdade != current_user.faculdade.id_faculdade:
        flash("Sem permissão.", "danger")
        return redirect(url_for("faculdade.listar_verificacoes"))

    estudante = Estudante(
        name=solicitacao.user.name,
        cpf=solicitacao.cpf,
        data_nascimento=solicitacao.data_nascimento,
        endereco=solicitacao.endereco,
        telefone=solicitacao.telefone,
        user=solicitacao.user,
    )

    solicitacao.user.status = UserStatus.VERIFICADO

    solicitacao.status = SolicitacaoStatus.APROVADA

    db.session.add(estudante)
    db.session.commit()

    flash("Aluno verificado com sucesso.", "success")
    return redirect(url_for("faculdade.listar_verificacoes"))


@faculdade_bp.route("/verificacoes/<string:id_solicitacao>/rejeitar", methods=["POST"])
@login_required
@roles_required(UserRole.FACULDADE)
def rejeitar_verificacao(id_solicitacao):
    solicitacao = SolicitacaoVerificacao.query.get_or_404(id_solicitacao)

    if solicitacao.id_faculdade != current_user.faculdade.id_faculdade:
        flash("Sem permissão.", "danger")
        return redirect(url_for("faculdade.listar_verificacoes"))

    solicitacao.status = SolicitacaoStatus.RECUSADA

    db.session.commit()

    flash("Solicitação rejeitada.", "warning")

    return redirect(url_for("faculdade.listar_verificacoes"))
