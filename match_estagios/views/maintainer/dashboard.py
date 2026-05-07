from flask.templating import render_template
from flask_login import login_required

from match_estagios.models.empresa import Empresa
from match_estagios.models.user import User, UserRole
from match_estagios.models.vaga import Vaga
from match_estagios.utils.decorators import roles_required

from . import maintainer_bp


@maintainer_bp.route("/")
@login_required
@roles_required(UserRole.MAINTAINER)
def dashboard():
    return render_template(
        "maintainer/dashboard.html",
        total_usuarios=User.query.count(),
        total_empresas=Empresa.query.count(),
        total_vagas=Vaga.query.count(),
        total_candidaturas=0,  # implementar
    )
