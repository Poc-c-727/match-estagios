from match_estagios.extensions import db


class Estudante(db.Model):
    __tablename__ = "estudantes"

    id_estudante = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(20), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))

    id_user = db.Column(
        db.BigInteger,
        db.ForeignKey("users.id_user", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Relacionamento (1:1)
    user = db.relationship("User", back_populates="estudante")

    def __init__(self, name, cpf, data_nascimento, endereco, telefone=None, user=None):
        self.name = name
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.telefone = telefone
        self.user = user
