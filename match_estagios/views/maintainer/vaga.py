from flask import flash, redirect, request, url_for
from flask.templating import render_template
from flask_login import login_required

from match_estagios.extensions import db
from match_estagios.forms.delete import DeleteForm
from match_estagios.forms.vaga import VagaForm
from match_estagios.models.user import UserRole
from match_estagios.models.vaga import Vaga, VagaModalidade, VagaStatus
from match_estagios.utils.decorators import roles_required

from . import maintainer_bp


@maintainer_bp.route("/vagas")
@login_required
@roles_required(UserRole.MAINTAINER)
def vagas():
    vagas = Vaga.query.order_by(Vaga.id_vaga.desc()).all()
    delete_form = DeleteForm()

    return render_template(
        "maintainer/vagas/vagas.html", vagas=vagas, delete_form=delete_form
    )


@maintainer_bp.route("/vagas/<int:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def editar_vaga(id):
    vaga = Vaga.query.get_or_404(id)
    form = VagaForm(obj=vaga)

    if request.method == "GET":
        form.modalidade.data = vaga.modalidade.name
        form.status.data = vaga.status.name

    if form.validate_on_submit():
        vaga.titulo = form.titulo.data
        vaga.descricao = form.descricao.data
        vaga.bolsa = form.bolsa.data
        vaga.modalidade = VagaModalidade[form.modalidade.data]
        vaga.status = VagaStatus[form.status.data]

        db.session.commit()

        flash("Vaga atualizada com sucesso.", "success")
        return redirect(url_for("maintainer.vagas"))

    return render_template(
        "maintainer/vagas/vaga_form.html",
        form=form,
        titulo="Editar vaga",
        botao="Salvar",
    )


@maintainer_bp.route("/vagas/<int:id>/deletar", methods=["POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def deletar_vaga(id):
    """Avaliar se poderá deletar uma vaga que tenha candidaturas"""

    vaga = Vaga.query.get_or_404(id)

    db.session.delete(vaga)
    db.session.commit()

    flash("Vaga deletada com sucesso.", "success")
    return redirect(url_for("maintainer.vagas"))
