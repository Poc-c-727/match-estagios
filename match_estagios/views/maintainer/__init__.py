from flask import Blueprint

maintainer_bp = Blueprint("maintainer", __name__, template_folder="templates")

from . import dashboard, empresa, usuario, vaga
