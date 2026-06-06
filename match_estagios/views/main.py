from flask import flash, redirect, request, url_for
from flask.blueprints import Blueprint
from flask.templating import render_template
from flask_login import current_user, login_required

from match_estagios.extensions import db
from match_estagios.forms.basic_form import BasicForm
from match_estagios.forms.verificacao import SolicitacaoVerificacaoForm
from match_estagios.models.candidatura import Candidatura, CandidaturaStatus
from match_estagios.models.faculdade import Faculdade
from match_estagios.models.user import User, UserRole, UserStatus
from match_estagios.models.vaga import Vaga, VagaStatus
from match_estagios.models.verificacao import SolicitacaoStatus, SolicitacaoVerificacao
from match_estagios.services.perfil_service import (
    choose_user_form,
    populate_form,
    save_form,
)
from match_estagios.utils.decorators import roles_required

main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
def index():
    # if current_user.is_authenticated:
    #     return render_template("index_logged.html")
    # Talve não seja necessário um "index_logged", um "redirecionador" para uma
    # tela adequada para cada usuário. Criei um arquivo `templates/index_logged.html`
    # para evitar que o código quebre se o código for descomentado.
    return render_template("index.html")


@main_bp.route("/sobre")
def sobre():
    return render_template("sobre.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("index_logged.html")


@main_bp.route("/perfil")
@login_required
def perfil():
    return render_template("main/perfil.html")


@main_bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    try:
        form = choose_user_form(current_user)
    except ValueError:
        flash("Tipo de usuário inválido", "danger")
        return redirect(url_for("main.perfil"))

    print("pegou formulário")
    if request.method == "GET":
        populate_form(form, current_user)

    if form.validate_on_submit():
        save_form(form, current_user)

        flash("Perfil atualizado", "success")
        return redirect(url_for("main.perfil"))

    if form.errors:
        print(form.errors)

    return render_template("main/editar_perfil.html", form=form)


@main_bp.route("/perfil/verificacao", methods=["GET", "POST"])
@login_required
@roles_required(UserRole.ESTUDANTE)
def solicitar_verificacao():

    if current_user.status != UserStatus.PENDENTE:
        flash("Sua conta já foi verificada.", "warning")
        return redirect(url_for("main.perfil"))

    form = SolicitacaoVerificacaoForm()

    faculdades = Faculdade.query.all()

    form.id_faculdade.choices = [
        (faculdade.id_faculdade, faculdade.name) for faculdade in faculdades
    ]

    if form.validate_on_submit():
        solicitacao_existente = SolicitacaoVerificacao.query.filter_by(
            id_user=current_user.id_user, status=SolicitacaoStatus.PENDENTE
        ).first()

        if solicitacao_existente:
            flash("Você já possui uma solicitação pendente.", "warning")
            return redirect(url_for("main.perfil"))

        print("solicitação enviada")
        solicitacao = SolicitacaoVerificacao(
            ra=form.ra.data,
            cpf=form.cpf.data,
            curso=form.curso.data,
            data_nascimento=form.data_nascimento.data,
            endereco=form.endereco.data,
            telefone=form.telefone.data,
            id_faculdade=form.id_faculdade.data,
            id_user=current_user.id_user,
        )
        print("instância da solicitação criada")

        db.session.add(solicitacao)
        db.session.commit()
        print("solicitação adicionada")

        flash("Solicitação enviada com sucesso.", "success")
        return redirect(url_for("main.perfil"))

    return render_template("main/solicitar_verificacao.html", form=form)


@main_bp.route("/vagas")
@login_required
def listar_vagas():
    vagas = Vaga.query.filter_by(status=VagaStatus.ABERTA).all()
    return render_template("main/vagas.html", vagas=vagas)


@main_bp.route("/vagas/<string:id>")
@login_required
def detalhes_vaga(id):
    form = BasicForm()
    vaga = Vaga.query.get_or_404(id)

    candidatura_existente = None

    if current_user.role == UserRole.ESTUDANTE and current_user.estudante:
        candidatura_existente = Candidatura.query.filter_by(
            id_estudante=current_user.estudante.id_estudante, id_vaga=vaga.id_vaga
        ).first()

    return render_template(
        "main/detalhes_vaga.html",
        form=form,
        vaga=vaga,
        candidatura_existente=candidatura_existente,
    )


@main_bp.route("/vagas/<string:id>/candidatar", methods=["POST"])
@login_required
@roles_required(UserRole.ESTUDANTE)
def candidatar(id):

    if current_user.status != UserStatus.VERIFICADO:
        flash("Sua conta precisa estar verificada", "danger")
        return redirect(url_for("main.detalhes_vaga", id=id))

    vaga = Vaga.query.get_or_404(id)
    id_estudante = current_user.estudante.id_estudante

    # 1. Verifica se a candidatura tradicional já existe
    candidatura_existente = Candidatura.query.filter_by(
        id_estudante=id_estudante,
        id_vaga=vaga.id_vaga,
    ).first()

    if candidatura_existente:
        flash("Você já se candidatou para esta vaga.", "warning")
        return redirect(url_for("main.detalhes_vaga", id=id))

    # 2. Cria a candidatura tradicional
    candidatura = Candidatura(
        id_estudante=id_estudante,
        id_vaga=vaga.id_vaga,
    )
    db.session.add(candidatura)

    # 3. SALVA O LIKE DO ESTUDANTE NA TABELA DE LIKES
    like_estudante = Like.query.filter_by(
        id_vaga=vaga.id_vaga,
        id_estudante=id_estudante,
        quem_curtiu='ESTUDANTE'
    ).first()

    if not like_estudante:
        novo_like = Like(id_vaga=vaga.id_vaga, id_estudante=id_estudante, quem_curtiu='ESTUDANTE')
        db.session.add(novo_like)

    # 4. CHECA SE A EMPRESA JÁ TINHA CURTIDO ESTE ESTUDANTE ANTES
    empresa_ja_curtiu = Like.query.filter_by(
        id_vaga=vaga.id_vaga,
        id_estudante=id_estudante,
        quem_curtiu='EMPRESA'
    ).first()

    db.session.commit()

    # 5. Exibe a mensagem correspondente
    if empresa_ja_curtiu:
        flash("🔥 DEU MATCH! A empresa dona desta vaga já tinha se interessado pelo seu perfil!", "success")
    else:
        flash("Candidatura realizada com sucesso! Se a empresa curtir você de volta, vocês darão Match.", "success")

    return redirect(url_for("main.detalhes_vaga", id=id))


@main_bp.route("/minhas-candidaturas")
@login_required
@roles_required(UserRole.ESTUDANTE)
def minhas_candidaturas():

    form = BasicForm()

    candidaturas = Candidatura.query.filter_by(
        id_estudante=current_user.estudante.id_estudante
    ).all()

    return render_template(
        "main/minhas_candidaturas.html", form=form, candidaturas=candidaturas
    )


@main_bp.route(
    "/minhas-candidaturas/<string:id_candidatura>/cancelar", methods=["POST"]
)
@login_required
@roles_required(UserRole.ESTUDANTE)
def cancelar_candidatura(id_candidatura):

    candidatura = Candidatura.query.get_or_404(id_candidatura)

    if candidatura.id_estudante != current_user.estudante.id_estudante:
        flash("Sem permissão.", "danger")
        return redirect(url_for("main.minhas_candidaturas"))

    if candidatura.status != CandidaturaStatus.PENDENTE:
        flash("Você não pode cancelar essa candidatura.", "warning")
        return redirect(url_for("main.minhas_candidaturas"))

    db.session.delete(candidatura)
    db.session.commit()

    flash("Candidatura cancelada.", "success")

    return redirect(url_for("main.minhas_candidaturas"))

@main_bp.route("/candidatos")
@login_required
@roles_required(UserRole.EMPRESA)
def listar_candidatos():
    candidatos = User.query.filter_by(
        role=UserRole.ESTUDANTE, 
        status=UserStatus.VERIFICADO
    ).all()
    
    vagas_empresa = []
    if current_user.empresa:
        vagas_empresa = Vaga.query.filter_by(id_empresa=current_user.empresa.id_empresa, status=VagaStatus.ABERTA).all()
    
    return render_template("main/candidatos.html", candidatos=candidatos, vagas_empresa=vagas_empresa, vaga=None)


#ROTA COM CONTEXTO DE VAGA (Para a busca ativa/discovery por vaga)
@main_bp.route("/vagas/<id_vaga>/candidatos")
@login_required
@roles_required(UserRole.EMPRESA)
def listar_candidatos_por_vaga(id_vaga):
    vaga = Vaga.query.get_or_404(id_vaga)
    candidatos = User.query.filter_by(
        role=UserRole.ESTUDANTE, 
        status=UserStatus.VERIFICADO
    ).all()
    
    return render_template("main/candidatos.html", candidatos=candidatos, vaga=vaga)

from match_estagios.models.like import Like 
from match_estagios.models.vaga import Vaga # Certifique-se de importar o modelo de Vaga se necessário

# 1. Mudamos a URL para receber também o id_vaga do contexto onde a empresa está navegando
@main_bp.route("/vagas/<id_vaga>/candidatos/<id_estudante>/curtir", methods=["POST"])
@login_required
@roles_required(UserRole.EMPRESA)
def curtir_candidato(id_vaga, id_estudante):
    
    # 2. Verifica se a empresa já curtiu esse candidato NESTA VAGA antes (para não duplicar)
    ja_curtiu = Like.query.filter_by(
        id_vaga=id_vaga, 
        id_estudante=id_estudante, 
        quem_curtiu='EMPRESA'
    ).first()

    if ja_curtiu:
        flash("Você já curtiu este candidato para esta vaga!", "info")
        # Ajuste o redirect para onde você preferir (ex: a lista de candidatos daquela vaga)
        return redirect(url_for("main.listar_candidatos", id_vaga=id_vaga))

    # 3. O SEGREDO DO MATCH: O estudante já curtiu ESSA VAGA específica antes?
    estudante_ja_curtiu = Like.query.filter_by(
        id_vaga=id_vaga, 
        id_estudante=id_estudante, 
        quem_curtiu='ESTUDANTE'
    ).first()

    # 4. Salva o novo like da empresa no banco usando id_vaga
    novo_like = Like(id_vaga=id_vaga, id_estudante=id_estudante, quem_curtiu='EMPRESA')
    db.session.add(novo_like)

    if estudante_ja_curtiu:
        # SE OS DOIS SE CURTIRAM NA MESMA VAGA: DEU MATCH!
        db.session.commit()
        flash("🔥 Deu MATCH! O candidato também se interessou por esta vaga!", "success")
    else:
        # Se só a empresa curtiu, salva silenciosamente
        db.session.commit()
        flash("Candidato curtido! Se ele curtir esta vaga de volta, vocês darão Match.", "success")

    return redirect(url_for("main.listar_candidatos", id_vaga=id_vaga))

from match_estagios.models.like import Like
from match_estagios.models.vaga import Vaga
from match_estagios.models.estudante import Estudante
from sqlalchemy import and_

@main_bp.route("/matches")
@login_required
def ver_matches():
    # Criamos um apelido (alias) para a tabela de likes para poder cruzá-la com ela mesma
    LikeEmpresa = db.aliased(Like)
    
    # Base da consulta: junta as tabelas para trazer o Like, os dados da Vaga e os dados do Estudante
    matches_query = db.session.query(Like, Vaga, Estudante).join(
        Vaga, Like.id_vaga == Vaga.id_vaga
    ).join(
        Estudante, Like.id_estudante == Estudante.id_estudante
    ).join(
        LikeEmpresa,
        and_(
            Like.id_vaga == LikeEmpresa.id_vaga,
            Like.id_estudante == LikeEmpresa.id_estudante,
            Like.quem_curtiu == 'ESTUDANTE',    # Lado do estudante
            LikeEmpresa.quem_curtiu == 'EMPRESA' # Lado da empresa
        )
    )

    # 🎛️ FILTRAGEM DINÂMICA POR USUÁRIO LOGADO
    if current_user.role.name == 'ESTUDANTE':
        # Se for estudante, mostra apenas os matches que pertencem ao ID dele
        matches = matches_query.filter(Like.id_estudante == current_user.estudante.id_estudante).all()
        
    elif current_user.role.name == 'EMPRESA':
        # Se for empresa, pega o ID de todas as vagas dela e traz os matches dessas vagas
        ids_vagas_empresa = [v.id_vaga for v in current_user.empresa.vagas]
        matches = matches_query.filter(Like.id_vaga.in_(ids_vagas_empresa)).all()
        
    else:
        matches = []

    return render_template("main/matches.html", matches=matches)