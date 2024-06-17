# schemas/usuarios.py

from pydantic import BaseModel
from datetime import datetime

class Usuarios(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
    data_criacao: datetime
    data_modificacao: datetime
