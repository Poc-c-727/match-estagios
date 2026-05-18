from .auth import auth_bp
from .company import company_bp
from .main import main_bp
from .maintainer import maintainer_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/")
    app.register_blueprint(company_bp, url_prefix="/empresa")
    app.register_blueprint(maintainer_bp, url_prefix="/mantenedor")
