from flask.blueprints import Blueprint
from flask_login import current_user, login_required

from match_estagios.models.user import UserRole
from match_estagios.utils.decorators import roles_required

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def root():
    if current_user.is_authenticated:
        return f"Logado como {current_user.email}"
    return "Não logado"


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.name}"


"""Exemplo de Rotas Protegidas"""


@main_bp.route("/admin")
@login_required
@roles_required(UserRole.ADMIN)
def admin_panel():
    return "Área do admin"


@main_bp.route("/empresa")
@login_required
@roles_required(UserRole.EMPRESA)
def empresa_panel():
    return "Área da empresa"


@main_bp.route("/admin_empresa")
@login_required
@roles_required(UserRole.ADMIN, UserRole.EMPRESA)
def admin_empresa_panel():
    return "Rota protegida da EMPRESA onde o ADMIN também pode acessar"
