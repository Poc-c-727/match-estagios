from datetime import datetime, timezone
from enum import Enum

from match_estagios.extensions import db
from match_estagios.utils.id import generate_short_uuid


class SolicitacaoStatus(Enum):
    PENDENTE = "pendente"
    APROVADA = "aprovada"
    RECUSADA = "recusada"


class SolicitacaoVerificacao(db.Model):
    __tablename__ = "solicitacoes_verificacao"

    __table_args__ = (
        db.UniqueConstraint(
            "id_user",
            "id_faculdade",
            name="uq_solicitacao_user_faculdade",
        ),
    )

    id_solicitacao = db.Column(
        db.String(22),
        primary_key=True,
        default=generate_short_uuid,
    )

    ra = db.Column(db.String(50), nullable=False)

    cpf = db.Column(db.String(20), nullable=False)

    curso = db.Column(db.String(255), nullable=False)

    data_nascimento = db.Column(db.Date, nullable=False)

    endereco = db.Column(db.String(255), nullable=False)

    telefone = db.Column(db.String(20))

    status = db.Column(
        db.Enum(SolicitacaoStatus),
        nullable=False,
        default=SolicitacaoStatus.PENDENTE,
    )

    data_solicitacao = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    id_user = db.Column(
        db.String(36),
        db.ForeignKey("users.id_user", ondelete="CASCADE"),
        nullable=False,
    )

    id_faculdade = db.Column(
        db.String(36),
        db.ForeignKey("faculdades.id_faculdade", ondelete="CASCADE"),
        nullable=False,
    )

    # Relacionamentos

    user = db.relationship("User", backref="solicitacoes_verificacao")

    faculdade = db.relationship(
        "Faculdade",
        backref="solicitacoes_verificacao",
    )

    def __init__(
        self,
        ra,
        cpf,
        curso,
        data_nascimento,
        endereco,
        id_faculdade,
        id_user,
        telefone=None,
    ):
        self.ra = ra
        self.cpf = cpf
        self.curso = curso
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.id_faculdade = id_faculdade
        self.id_user = id_user
