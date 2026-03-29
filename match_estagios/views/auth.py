from crypt import methods

from flask.blueprints import Blueprint
from flask.globals import request
from flask.helpers import flash, redirect, url_for
from flask.templating import render_template
from flask_login import login_user, logout_user

from match_estagios.extensions import bcrypt, db
from match_estagios.forms.auth import LoginForm, RegisterForm
from match_estagios.models.user import User, UserRole

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("Form submetido:", form.is_submitted())
        # Verifica se já existe
        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email já cadastrado", "danger")
            return redirect(url_for("auth.register"))

        # Cria usuário
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=bcrypt.generate_password_hash(form.password.data, 12).decode(
                "utf-8"
            ),
            role=UserRole.ESTUDANTE,  # padrão
        )

        db.session.add(user)
        db.session.commit()
        flash("Usuário cadastrado com sucesso!", "success")
        print("Form válido:", form.validate())
        return redirect(url_for("auth.login"))

    else:
        print("Erros:", form.errors)
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not bcrypt.check_password_hash(
            user.password_hash, form.password.data
        ):
            flash("Email ou senha incorretos", "danger")
            return redirect(url_for("auth.login"))
        else:
            # flash("Login realizado com sucesso", "success")
            login_user(user)

            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.root"))

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Logout realizado", "info")
    return redirect(url_for("auth.login"))
