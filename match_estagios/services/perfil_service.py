from match_estagios.extensions import db
from match_estagios.forms.perfis import (
    EmpresaPerfilForm,
    EstudantePerfilForm,
    FaculdadePerfilForm,
    UserPerfilForm,
)
from match_estagios.models.user import UserRole


def choose_user_form(user):
    match user.role:
        case UserRole.ESTUDANTE:
            if user.estudante:
                form = EstudantePerfilForm()
            else:
                form = UserPerfilForm()
        case UserRole.EMPRESA:
            form = EmpresaPerfilForm()
        case UserRole.FACULDADE:
            form = FaculdadePerfilForm()
        case _:
            raise ValueError(f"Role inválido: {user.role}")

    return form


def populate_form(form, user):
    form.name.data = user.name
    form.email.data = user.email

    match user.role:
        case UserRole.ESTUDANTE:
            if user.estudante:
                estudante = user.estudante

                form.cpf.data = estudante.cpf
                form.data_nascimento.data = estudante.data_nascimento
                form.endereco.data = estudante.endereco
                form.telefone.data = estudante.telefone

        case UserRole.EMPRESA:
            empresa = user.empresa

            if not empresa:
                return

            form.cnpj.data = empresa.cnpj
            form.ramo.data = empresa.ramo
            form.endereco.data = empresa.endereco
            form.site.data = empresa.site
            form.descricao.data = empresa.descricao

        case UserRole.FACULDADE:
            faculdade = user.faculdade

            if not faculdade:
                return

            form.cnpj.data = faculdade.cnpj
            form.site.data = faculdade.site
            form.telefone.data = faculdade.telefone


def save_form(form, user):
    user.name = form.name.data
    user.email = form.email.data

    match user.role:
        case UserRole.ESTUDANTE:
            if user.estudante:
                estudante = user.estudante

                estudante.name = form.name.data
                estudante.cpf = form.cpf.data
                estudante.data_nascimento = form.data_nascimento.data
                estudante.endereco = form.endereco.data
                estudante.telefone = form.telefone.data

        case UserRole.EMPRESA:
            empresa = user.empresa

            if not empresa:
                return

            empresa.name = form.name.data
            empresa.cnpj = form.cnpj.data
            empresa.ramo = form.ramo.data
            empresa.endereco = form.endereco.data
            empresa.site = form.site.data
            empresa.descricao = form.descricao.data

        case UserRole.FACULDADE:
            faculdade = user.faculdade

            if not faculdade:
                return

            faculdade.name = form.name.data
            faculdade.cnpj = form.cnpj.data
            faculdade.site = form.site.data
            faculdade.telefone = form.telefone.data

    db.session.commit()
