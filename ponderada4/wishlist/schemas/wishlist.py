# schemas/usuarios.py

from pydantic import BaseModel
from datetime import datetime

class Wishlist(BaseModel):
    id : int
    id_cliente : int
    id_produto : int
    data : datetime
    # id = Column(Integer, primary_key=True)
    # id_cliente = Column(Integer)
    # id_produto = Column(Integer)
    # data = Column(DateTime)

    class Config:
        orm_mode = True