from . import db
from .base import ModeloBase


class Jogador(ModeloBase):
     __tablename__ = "jogadores"
     nome = db.Column(db.String(200), nullable=False)
     posicao = db.Column(db.String(50))
     clube = db.Column(db.String(50))
     cabeceio = db.Column(db.Integer, default = 0)
     forca = db.Column(db.Integer, default = 0)

     @property
     def media(self):
        return (self.cabeceio + self.forca) / 2

     @classmethod
     def listar(cls):
        return cls.query.order_by(cls.posicao, cls.nome).all()
