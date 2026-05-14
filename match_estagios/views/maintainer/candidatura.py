from flask.templating import render_template
from flask_login.utils import login_required

from match_estagios.forms.basic_form import BasicForm
from match_estagios.models.candidatura import Candidatura, CandidaturaStatus
from match_estagios.models.user import UserRole
from match_estagios.models.vaga import Vaga
from match_estagios.utils.decorators import roles_required

from . import maintainer_bp


@maintainer_bp.route("/candidaturas")
@login_required
@roles_required(UserRole.MAINTAINER)
def candidaturas():

    vagas = Vaga.query.join(Candidatura).distinct().all()

    return render_template("maintainer/candidaturas/candidaturas.html", vagas=vagas)


@maintainer_bp.route("/candidaturas/<string:id_vaga>")
@login_required
@roles_required(UserRole.MAINTAINER)
def detalhes_candidaturas(id_vaga):
    form = BasicForm()
    vaga = Vaga.query.get_or_404(id_vaga)

    candidaturas = Candidatura.query.filter_by(id_vaga=id_vaga).all()

    return render_template(
        "company/detalhes_candidaturas.html",
        form=form,
        vaga=vaga,
        candidaturas=candidaturas,
        candidatura_status=CandidaturaStatus,
    )
