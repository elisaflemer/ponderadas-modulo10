# src/services/usuarios.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.wishlist import WishlistRepository
from models.wishlist import Wishlist
from schemas.wishlist import Wishlist as WishlistSchema

class WishlistService:
    def __init__(self):
        self.repository = WishlistRepository()

    def get(self, wishlist_id, db: AsyncSession):
        wishlist = self.repository.get(wishlist_id, db)
        if wishlist is None:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return wishlist

    def get_all(self, db: AsyncSession):
        return self.repository.get_all(db)

    def add(self, wishlist : WishlistSchema, db: AsyncSession):
        wishlist = Wishlist(**wishlist.dict(db))
        return self.repository.add(wishlist)

    def update(self, wishlist_id, wishlist : WishlistSchema, db: AsyncSession):
        wishlist = Wishlist(**wishlist.dict())
        return self.repository.update(wishlist_id, wishlist, db)

    def delete(self, wishlist_id, db: AsyncSession):
        return self.repository.delete(wishlist_id, db)