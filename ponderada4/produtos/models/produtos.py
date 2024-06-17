# usuarios.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from databases.database import Base
from sqlalchemy.sql import func

class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Integer)
    quantidade = Column(Integer)
    data_criacao = Column(DateTime, default=func.now())
    data_modificacao = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Produto(nome='{self.nome}', descricao='{self.descricao}, id={self.id}', preco='{self.preco}', quantidade='{self.quantidade}', criado_em='{self.data_criacao}', modificado_em='{self.data_modificacao}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'data_criacao': self.data_criacao,
            'data_modificacao': self.data_modificacao
        }