from enum import Enum

from match_estagios.extensions import db
from match_estagios.utils.id import generate_short_uuid


class VagaStatus(Enum):
    ABERTA = "aberta"
    PAUSADA = "pausada"
    FECHADA = "fechada"
    PREENCHIDA = "preenchida"


class VagaModalidade(Enum):
    REMOTO = "remoto"
    PRESENCIAL = "presencial"
    HIBRIDO = "hibrido"


class Vaga(db.Model):
    __tablename__ = "vagas"

    id_vaga = db.Column(db.String(22), primary_key=True, default=generate_short_uuid)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    bolsa = db.Column(db.Numeric(10, 2), nullable=False)

    modalidade = db.Column(db.Enum(VagaModalidade), nullable=False)
    status = db.Column(db.Enum(VagaStatus), nullable=False)

    id_empresa = db.Column(
        db.String(36), db.ForeignKey("empresas.id_empresa"), nullable=False
    )

    empresa = db.relationship("Empresa", backref="vagas")
    candidaturas = db.relationship(
        "Candidatura", back_populates="vaga", cascade="all, delete-orphan"
    )
