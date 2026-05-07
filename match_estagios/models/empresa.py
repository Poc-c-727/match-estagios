from match_estagios.extensions import db


class Empresa(db.Model):
    __tablename__ = "empresas"

    id_empresa = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cnpj = db.Column(db.String(20), unique=True, nullable=False)
    ramo = db.Column(db.String(255), nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    site = db.Column(db.String(255))
    descricao = db.Column(db.Text)

    id_user = db.Column(
        db.BigInteger, db.ForeignKey("users.id_user"), unique=True, nullable=False
    )

    # Relacionamento (1:1)
    user = db.relationship("User", back_populates="empresa", single_parent=True)

    def __init__(
        self, name, cnpj, ramo, endereco, site=None, descricao=None, user=None
    ):
        self.name = name
        self.cnpj = cnpj
        self.ramo = ramo
        self.endereco = endereco
        self.site = site
        self.descricao = descricao
        self.user = user
