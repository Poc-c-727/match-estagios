from datetime import datetime, timezone
from enum import Enum

from match_estagios.extensions import db
from match_estagios.utils.id import generate_short_uuid


class CandidaturaStatus(Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"


class Candidatura(db.Model):
    __tablename__ = "candidaturas"

    __table_args__ = (
        db.UniqueConstraint(
            "id_estudante", "id_vaga", name="uq_candidatura_estudante_vaga"
        ),
    )

    id_candidatura = db.Column(
        db.String(22), primary_key=True, default=generate_short_uuid
    )

    status = db.Column(
        db.Enum(CandidaturaStatus), nullable=False, default=CandidaturaStatus.PENDENTE
    )

    data_candidatura = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    id_estudante = db.Column(
        db.String(36),
        db.ForeignKey("estudantes.id_estudante"),
        nullable=False,
    )

    id_vaga = db.Column(
        db.String(22),
        db.ForeignKey("vagas.id_vaga"),
        nullable=False,
    )

    # Relacionamentos

    estudante = db.relationship("Estudante", back_populates="candidaturas")

    vaga = db.relationship("Vaga", back_populates="candidaturas")

    def __init__(self, id_estudante, id_vaga):
        self.id_estudante = id_estudante
        self.id_vaga = id_vaga
