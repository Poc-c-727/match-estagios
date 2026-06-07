from match_estagios.extensions import db
from match_estagios.utils.id import generate_uuid


class Estudante(db.Model):
    __tablename__ = "estudantes"

    id_estudante = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    curso = db.Column(db.String(150), nullable=True)
    semestre = db.Column(db.Integer, nullable=True)
    disponibilidade = db.Column(db.String(50), nullable=True)
    area_interesse = db.Column(db.String(100), nullable=True)
    curriculo_texto = db.Column(db.Text, nullable=True)

    id_user = db.Column(
        db.String(36),
        db.ForeignKey("users.id_user", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Relacionamento (1:1)
    user = db.relationship("User", back_populates="estudante")

    candidaturas = db.relationship(
        "Candidatura",
        back_populates="estudante",
        cascade="all, delete-orphan",
    )

    # CONSTRUTOR ATUALIZADO:
    # Definimos os novos parâmetros como None por padrão para não quebrar os cadastros antigos!
    def __init__(
        self, 
        name, 
        cpf, 
        data_nascimento, 
        endereco, 
        telefone=None, 
        user=None,
        curso=None,
        semestre=None,
        disponibilidade=None,
        area_interesse=None,
        curriculo_texto=None
    ):
        self.name = name
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.user = user
        
        # Inicializando os novos campos
        self.curso = curso
        self.semestre = semestre
        self.disponibilidade = disponibilidad
        self.area_interesse = area_interesse
        self.curriculo_texto = curriculo_texto