from match_estagios.extensions import db
from datetime import datetime

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    
    id_vaga = db.Column(db.String(36), db.ForeignKey('vagas.id_vaga'), nullable=False)
    id_estudante = db.Column(db.String(36), db.ForeignKey('estudantes.id_estudante'), nullable=False)
    
    quem_curtiu = db.Column(db.String(20), nullable=False) 
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)