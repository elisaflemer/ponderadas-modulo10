# schemas/usuarios.py

from pydantic import BaseModel
from datetime import datetime

class Wishlist(BaseModel):
    id : int
    id_cliente : int
    id_produto : int
    data : datetime

    class Config:
        orm_mode = True