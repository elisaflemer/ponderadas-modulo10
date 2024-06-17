
from pydantic import BaseModel
from datetime import datetime

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    quantidade: int
    data_criacao: datetime
    data_modificacao: datetime

    class Config:
        orm_mode = True