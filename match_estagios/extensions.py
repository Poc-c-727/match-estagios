from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

bcrypt = Bcrypt()
bootstrap = Bootstrap5()
migrate = Migrate()
db = SQLAlchemy()
csrf_protect = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"  # type: ignore
