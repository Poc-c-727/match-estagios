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

    area = db.Column(db.String(100), nullable=True)
    disponibilidade = db.Column(db.String(50), nullable=True)

    empresa = db.relationship("Empresa", backref="vagas")
    candidaturas = db.relationship(
        "Candidatura", back_populates="vaga", cascade="all, delete-orphan"
    )

    # CONSTRUTOR ATUALIZADO:
    # Definimos como None por padrão para não quebrar a criação de vagas antigas em testes ou seeders
    def __init__(self, titulo, descricao, bolsa, modalidade, status, id_empresa, area=None, disponibilidade=None):
        self.titulo = titulo
        self.descricao = descricao
        self.bolsa = bolsa
        self.modalidade = modalidade
        self.status = status
        self.id_empresa = id_empresa
        
        # Inicializando os novos campos de filtro
        self.area = area
        self.disponibilidade = disponibilidade