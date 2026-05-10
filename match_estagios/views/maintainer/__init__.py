from flask import Blueprint

maintainer_bp = Blueprint("maintainer", __name__, template_folder="templates")

from . import candidatura, dashboard, empresa, usuario, vaga
