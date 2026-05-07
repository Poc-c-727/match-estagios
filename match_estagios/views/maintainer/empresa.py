from flask import flash, redirect, render_template, url_for
from flask_login import login_required

from match_estagios.extensions import bcrypt, db
from match_estagios.forms.criar_empresa import MaintainerEmpresaForm
from match_estagios.forms.delete import DeleteForm
from match_estagios.forms.empresa import EmpresaForm
from match_estagios.models.empresa import Empresa
from match_estagios.models.user import User, UserRole, UserStatus
from match_estagios.utils.decorators import roles_required

from . import maintainer_bp


@maintainer_bp.route("/empresas")
@login_required
@roles_required(UserRole.MAINTAINER)
def empresas():
    empresas = Empresa.query.order_by(Empresa.id_empresa.desc()).all()
    delete_form = DeleteForm()

    return render_template(
        "maintainer/empresas/empresas.html", empresas=empresas, delete_form=delete_form
    )


@maintainer_bp.route("/empresas/criar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def criar_empresa():
    """
    To-do:
        - quando o formulário for enviado e o email ou cnpj já existir não apagar todos os dados já inseridos
    """
    form = MaintainerEmpresaForm()

    if form.validate_on_submit():
        # verifica se já existe email
        email = User.query.filter_by(email=form.email.data).first()
        if email:
            flash("Email já cadastrado", "danger")
            return render_template("maintainer/empresas/criar_empresa.html", form=form)

        # verifica se já existe o cnpj cadastrado
        cnpj = Empresa.query.filter_by(cnpj=form.cnpj.data).first()
        if cnpj:
            flash(f'O CNPJ "{form.cnpj.data}" já foi cadastrado no sistema', "danger")
            return render_template("maintainer/empresas/criar_empresa.html", form=form)

        # criação de usuário
        user = User(
            name=form.user_name.data,
            email=form.email.data,
            password_hash=bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            ),
            role=UserRole.EMPRESA,
            status=UserStatus.VERIFICADO,
        )

        # Criação da empresa
        empresa = Empresa(
            name=form.name.data,
            cnpj=form.cnpj.data,
            ramo=form.ramo.data,
            endereco=form.endereco.data,
            site=form.site.data,
            descricao=form.descricao.data,
            user=user,
        )
        try:
            db.session.add(user)
            db.session.add(empresa)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Erro ao criar empresa", "danger")
            return render_template("maintainer/empresas/criar_empresa.html", form=form)

        flash("Empresa e usuário criados com sucesso.", "success")
        return redirect(url_for("maintainer.empresas"))

    return render_template("maintainer/empresas/criar_empresa.html", form=form)


@maintainer_bp.route("/empresas/<int:id_empresa>/editar", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def editar_empresa(id_empresa):
    empresa = Empresa.query.get_or_404(id_empresa)

    form = EmpresaForm(obj=empresa)

    if form.validate_on_submit():
        empresa.name = form.name.data
        empresa.cnpj = form.cnpj.data
        empresa.ramo = form.ramo.data
        empresa.endereco = form.endereco.data
        empresa.site = form.site.data
        empresa.descricao = form.descricao.data

        db.session.commit()

        flash("Empresa atualizada com sucesso!", "success")
        return redirect(url_for("maintainer.empresas"))

    return render_template("maintainer/empresas/editar_empresa.html", form=form)


# A rota de deletar a empresa pode deletar vagas e usuários vinculadas
# No futuro:
#   - impedir a remoção se a empresa tem vagas
#   - soft delete
@maintainer_bp.route("/empresas/<int:id_empresa>/deletar", methods=["POST"])
@login_required
@roles_required(UserRole.MAINTAINER)
def deletar_empresa(id_empresa):
    empresa = Empresa.query.get_or_404(id_empresa)

    if empresa.vagas:
        flash("Você não pode deletar empresas com vagas", "danger")
        return redirect(url_for("maintainer.empresas"))

    db.session.delete(empresa.user)
    db.session.delete(empresa)
    db.session.commit()

    flash("Empresa deletada com sucesso.", "success")
    return redirect(url_for("maintainer.empresas"))
