# src/services/usuarios.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from repository.wishlist import WishlistRepository
from models.wishlist import Wishlist
from schemas.wishlist import Wishlist as WishlistSchema

class WishlistService:
    def __init__(self):
        self.repository = WishlistRepository()

    def get(self, wishlist_id):
        wishlist = self.repository.get(wishlist_id)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return wishlist

    def get_all(self):
        return self.repository.get_all()

    def add(self, wishlist : WishlistSchema):
        wishlist = Wishlist(**wishlist.dict())
        return self.repository.add(wishlist)

    def update(self, wishlist_id, wishlist : WishlistSchema):
        wishlist = Wishlist(**wishlist.dict())
        return self.repository.update(wishlist_id, wishlist)

    def delete(self, wishlist_id):
        return self.repository.delete(wishlist_id)