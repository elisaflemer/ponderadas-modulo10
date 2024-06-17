# produtos.py
from sqlalchemy import Column, Integer, String, Double, DateTime
from databases.database import Base
from sqlalchemy.sql import func

class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer)
    id_produto = Column(Integer)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now() )

    def to_dict(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'id_produto': self.id_produto,
            'data_criacao': self.data_criacao,
            'data_atualizacao': self.data_atualizacao
        }