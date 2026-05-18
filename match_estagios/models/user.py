from datetime import datetime, timezone
from enum import Enum

from flask_login import UserMixin

from match_estagios.extensions import db
from match_estagios.utils.id import generate_uuid


class UserRole(Enum):
    MAINTAINER = "mantenedor"
    ESTUDANTE = "estudante"
    EMPRESA = "empresa"
    FACULDADE = "faculdade"


class UserStatus(Enum):
    PENDENTE = "pendente"
    VERIFICADO = "verificado"
    REJEITADO = "rejeitado"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id_user = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    status = db.Column(db.Enum(UserStatus), nullable=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relacionamentos
    estudante = db.relationship(
        "Estudante", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    empresa = db.relationship(
        "Empresa", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    faculdade = db.relationship(
        "Faculdade", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __init__(self, name, email, password_hash, role, status):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.status = status

    def get_id(self):
        return str(self.id_user)
