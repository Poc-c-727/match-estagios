from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from match_estagios.extensions import bcrypt, db
from match_estagios.forms.delete import DeleteForm
from match_estagios.forms.editar_usuario import MaintainerUsuarioForm
from match_estagios.forms.usuario import UsuarioForm
from match_estagios.models.user import User, UserRole, UserStatus
from match_estagios.utils.decorators import roles_required

from . import maintainer_bp


@maintainer_bp.route("/usuarios")
@login_required
@roles_required(UserRole.MAINTAINER)
def usuarios():
    usuarios = User.query.order_by(User.id_user.desc()).all()
    delete_form = DeleteForm()

    return render_template(
        "maintainer/usuarios/usuario.html", usuarios=usuarios, delete_form=delete_form
    )


@maintainer_bp.route("/usuarios/criar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def criar_usuario():
    form = UsuarioForm()

    if form.validate_on_submit():
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash("Email já cadastrado", "danger")
            return render_template("maintainer/usuarios/criar_usuario.html", form=form)

        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            ),
            role=UserRole[form.role.data],
            status=UserStatus[form.status.data],
        )

        db.session.add(user)
        db.session.commit()

        flash("Usuário criado com sucesso.", "success")
        return redirect(url_for("maintainer.usuarios"))

    return render_template(
        "maintainer/usuarios/usuario_form.html",
        form=form,
        titulo="Criar usuário",
        botao="Criar",
        is_edit=False,
    )


@maintainer_bp.route("/usuarios/<string:id>/editar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def editar_usuario(id):
    user = User.query.get_or_404(id)
    form = MaintainerUsuarioForm(obj=user)

    # será que precisa desse if?
    if request.method == "GET":
        form.role.data = user.role.name
        form.status.data = user.status.name

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.role = UserRole[form.role.data]
        user.status = UserStatus[form.status.data]

        if form.password.data:
            user.password_hash = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")

        db.session.commit()

        flash("Usuário atualizado com sucesso", "success")
        return redirect(url_for("maintainer.usuarios"))

    return render_template(
        "maintainer/usuarios/usuario_form.html",
        form=form,
        titulo="Editar usuário",
        botao="Salvar",
        is_edit=True,
    )


@maintainer_bp.route("/usuarios/<string:id>/deletar", methods=["POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def deletar_usuario(id):
    user = User.query.get_or_404(id)

    # Permitir que o usuário possa ser deletado mesmo com faculdade ou empresa vinculada?
    # Se sim, então deletar a faculdade ou empresa junto?
    # if user.empresa:
    #     flash("Não é possível deletar usuário com empresa vinculada", "danger")
    #     return redirect(url_for("maintainer.usuarios"))

    # if user.faculdade:
    #     flash("Não é possível deletar usuário com faculdade vinculada", "danger")
    #     return redirect(url_for("maintainer.usuarios"))

    db.session.delete(user)
    db.session.commit()

    flash("Usuário deletado com sucesso.", "success")
    return redirect(url_for("maintainer.usuarios"))
