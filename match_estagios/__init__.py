from dotenv import load_dotenv
from flask import Flask

from match_estagios.models.user import User

from .commands.db_commands import register_commands
from .config import Config
from .extensions import bcrypt, bootstrap, csrf_protect, db, login_manager, migrate

load_dotenv()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


def format_currency(value):
    if value is None:
        return "0,00"
    return (
        "R$ {:,.2f}".format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    )


def create_app():
    # Instantiate Flask
    app = Flask(__name__)

    # Load environment specific settings
    app.config.from_object(Config)

    # Blueprints
    from .views import register_blueprints

    register_blueprints(app)

    # CLI commands
    register_commands(app)

    # Extensions
    db.init_app(app)  # Flask-SQLAlchemy
    migrate.init_app(app, db)  # Flask-Migrate
    bootstrap.init_app(app)  # bootstrap-flask
    bcrypt.init_app(app)  # Flask-Bcrypt
    csrf_protect.init_app(app)  # WTForms CSRFProtect
    login_manager.init_app(app)  # Flask-Login

    login_manager.login_view = "auth.login"  # type: ignore (pro meu editor de código T.T)

    from . import models

    app.jinja_env.filters["currency"] = format_currency

    return app
