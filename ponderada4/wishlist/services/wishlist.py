# src/services/usuarios.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.wishlist import WishlistRepository
from models.wishlist import Wishlist
from schemas.wishlist import Wishlist as WishlistSchema
from logs.logs import log_info, log_error, log_warning

class WishlistService:
    def __init__(self):
        self.repository = WishlistRepository()

    async def get(self, wishlist_id, db: AsyncSession):
        wishlist = await self.repository.get(wishlist_id, db)
        if wishlist is None:
            log_error("Wishlist não encontrada")
            raise HTTPException(status_code=404, detail="Wishlist não encontrada")
        return wishlist

    async def get_all(self, db: AsyncSession):
        wishlists = await self.repository.get_all(db)
        if not wishlists:
            log_warning("Nenhuma wishlist encontrada")
            raise HTTPException(status_code=404, detail="Nenhuma wishlist encontrada")
    

    async def add(self, wishlist : WishlistSchema, db: AsyncSession):
        wishlist = await Wishlist(**wishlist.dict(db))
        return self.repository.add(wishlist)

    async def update(self, wishlist_id, wishlist : WishlistSchema, db: AsyncSession):
        wishlist = await Wishlist(**wishlist.dict())
        return self.repository.update(wishlist_id, wishlist, db)

    async def delete(self, wishlist_id, db: AsyncSession):
        wishlist = await self.repository.get(wishlist_id, db)
        if wishlist is None:
            log_error("Wishlist não encontrada")
            raise HTTPException(status_code=404, detail="Wishlist não encontrada")
        
        return await self.repository.delete(wishlist_id, db)