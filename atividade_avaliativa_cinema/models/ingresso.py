from . import db
from .base import ModeloBase


class Ingresso(ModeloBase):
    """Compra de ingresso para uma sessão (ponto extra)."""

    __tablename__ = "ingressos"

    sessao_id = db.Column(db.Integer, db.ForeignKey("sessoes.id"), nullable=False)
    assento = db.Column(db.String(10), nullable=False)
    nome_comprador = db.Column(db.String(120), nullable=False)

    sessao = db.relationship("Sessao", back_populates="ingressos")

    def __repr__(self):
        return f"<Ingresso {self.assento} - {self.nome_comprador}>"
