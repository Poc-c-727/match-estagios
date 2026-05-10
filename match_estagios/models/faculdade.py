from match_estagios.extensions import db
from match_estagios.utils.id import generate_uuid


class Faculdade(db.Model):
    __tablename__ = "faculdades"

    id_faculdade = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    site = db.Column(db.String(255))
    telefone = db.Column(db.String(20))

    id_user = db.Column(
        db.String(36),
        db.ForeignKey("users.id_user", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Relacionamento (1:1)
    user = db.relationship("User", back_populates="faculdade")

    def __init__(self, name, cnpj, site=None, telefone=None, user=None):
        self.name = name
        self.cnpj = cnpj
        self.site = site
        self.telefone = telefone
        self.user = user
