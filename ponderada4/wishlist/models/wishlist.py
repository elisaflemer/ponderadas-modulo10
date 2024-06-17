# produtos.py
from sqlalchemy import Column, Integer, String, Double, DateTime
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

class Wishlist(Base):
    __tablename__ = 'wishlist'

    id = Column(Integer, primary_key=True)
    id_cliente = Column(Integer)
    id_produto = Column(Integer)
    data = Column(DateTime)

    def __init__(self, id_cliente, id_produto, data):
        self.id_cliente = id_cliente
        self.id_produto = id_produto
        self.data = data

    def to_dict(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'id_produto': self.id_produto,
            'data': self.data
        }