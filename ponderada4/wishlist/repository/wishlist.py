# src/repository/wishlist.py

from models.wishlist import Wishlist
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select, update
from datetime import datetime
from schemas.wishlist import Wishlist as WishlistSchema

class WishlistRepository:
    def __init__(self):
        pass

    async def get(self, wishlist_id: int, db: AsyncSession):
        stmt = select(Wishlist).where(Wishlist.id == wishlist_id)
        result = await db.execute(stmt)
        result = result.scalars().first()
        return result
    
    async def get_all(self, db: AsyncSession):
        stmt = select(Wishlist)
        result = await db.execute(stmt)
        result = result.scalars().all()
        return

    async def add(self, wishlist: Wishlist, db: AsyncSession):
        wishlist.created_at = datetime.now()
        db.add(wishlist)
        await db.commit()
        return wishlist

    async def update(self, wishlist_id: int, wishlist: WishlistSchema, db: AsyncSession):
        wishlist_db = await db.get(Wishlist, wishlist_id)
        if wishlist_db is None:
            return {"message": "Wishlist not found"}
        wishlist_db.id_cliente = wishlist.id_cliente
        wishlist_db.id_produto = wishlist.id_produto
        await db.commit()
        return wishlist_db

    async def delete(self, wishlist_id: int, db: AsyncSession):
        wishlist = await db.get(Wishlist, wishlist_id)
        if wishlist is None:
            return {"message": "Wishlist not found"}
        db.delete(wishlist)
        await db.commit()
        return {"message": "Wislist deleted"}