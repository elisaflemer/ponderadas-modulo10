# usuarios.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from databases.database import Base
from sqlalchemy.sql import func

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    data_criacao = Column(DateTime, default=func.now())
    data_modificacao = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', email='{self.email}, id={self.id}', criado_em='{self.data_criacao}', modificado_em='{self.data_modificacao}')>"

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'data_criacao': self.data_criacao,
            'data_modificacao': self.data_modificacao
        }