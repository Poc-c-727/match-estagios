from datetime import datetime, timezone

from match_estagios.extensions import db
from match_estagios.utils.id import generate_short_uuid


class Notificacao(db.Model):
    __tablename__ = "notificacoes"

    id_notificacao = db.Column(
        db.String(22),
        primary_key=True,
        default=generate_short_uuid,
    )

    titulo = db.Column(db.String(255), nullable=False)

    mensagem = db.Column(db.Text, nullable=False)

    lida = db.Column(db.Boolean, default=False, nullable=False)

    data_criacao = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    id_user = db.Column(
        db.String(36),
        db.ForeignKey("users.id_user", ondelete="CASCADE"),
        nullable=False,
    )

    user = db.relationship("User", backref="notificacoes")
