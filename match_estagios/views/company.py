from flask import flash, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required
from werkzeug.utils import redirect

from match_estagios.extensions import db
from match_estagios.forms.delete import DeleteForm
from match_estagios.forms.vaga import VagaForm
from match_estagios.models.user import UserRole
from match_estagios.models.vaga import Vaga, VagaModalidade, VagaStatus
from match_estagios.utils.decorators import roles_required

company_bp = Blueprint("company", __name__, template_folder="templates")


@company_bp.route("/", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.EMPRESA)
def index():
    return render_template("company/index.html")


@company_bp.route("/vaga/criar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.EMPRESA)
def criar_vaga():
    form = VagaForm()

    if form.validate_on_submit():
        if not current_user.empresa:
            flash("Usuário não possui empresa associada", "danger")
            return redirect(url_for("company.index"))

        vaga = Vaga(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            bolsa=form.bolsa.data,
            modalidade=VagaModalidade[form.modalidade.data],
            status=VagaStatus[form.status.data],
            id_empresa=current_user.empresa.id_empresa,
        )

        db.session.add(vaga)
        db.session.commit()

        flash("Vaga criada com sucesso!", "success")
        return redirect(url_for("company.index"))

    return render_template("company/criar_vaga.html", form=form)


@company_bp.route("/vagas")
@login_required
@roles_required(UserRole.EMPRESA)
def listar_vagas():
    if not current_user.empresa:
        flash("Usuário não possui empresa associada", "danger")
        return redirect(url_for("main.index"))

    vagas = current_user.empresa.vagas
    delete_form = DeleteForm()

    return render_template("company/vagas.html", vagas=vagas, delete_form=delete_form)


@company_bp.route("/vaga/<int:id_vaga>/editar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.EMPRESA)
def editar_vaga(id_vaga):
    vaga = Vaga.query.get_or_404(id_vaga)

    if vaga.id_empresa != current_user.empresa.id_empresa:
        flash("Você não tem premissão para editar esta vaga", "danger")
        return redirect(url_for("company.listar_vagas"))

    form = VagaForm(obj=vaga)

    if form.validate_on_submit():
        vaga.titulo = form.titulo.data
        vaga.descricao = form.descricao.data
        vaga.bolsa = form.bolsa.data
        vaga.modalidade = VagaModalidade[form.modalidade.data]
        vaga.status = VagaStatus[form.status.data]

        db.session.commit()

        flash("Vaga atualizada com sucesso", "success")
        return redirect(url_for("company.listar_vagas"))

    return render_template("company/editar_vaga.html", form=form, vaga=vaga)


@company_bp.route("/vaga/<int:id_vaga>/deletar", methods=["POST"])
@login_required
@roles_required(UserRole.EMPRESA)
def deletar_vaga(id_vaga):
    vaga = Vaga.query.get_or_404(id_vaga)

    if vaga.id_empresa != current_user.empresa.id_empresa:
        flash("Você não tem permição para deletar esta vaga", "danger")
        return redirect(url_for("company.listar_vagas"))

    db.session.delete(vaga)
    db.session.commit()

    flash("Vaga deletada com sucesso!", "success")
    return redirect(url_for("company.listar_vagas"))
