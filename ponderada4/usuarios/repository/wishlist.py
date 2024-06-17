# src/repository/wishlist.py

from models.wishlist import Wishlist
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from datetime import datetime

class WishlistRepository:
    def __init__(self):
        pass

    async def get(self, wishlist_id: int, db: AsyncSession):
        return await db.get(Wishlist, wishlist_id)

    async def get_all(self, db: AsyncSession):
        result = await db.execute(select(Wishlist))
        return result.scalars().all()

    async def add(self, wishlist: Wishlist, db: AsyncSession):
        wishlist.id = None
        wishlist.creation_date = datetime.now()
        db.add(wishlist)
        await db.flush()
        await db.commit()
        return {"message": "Wishlist added successfully"}

    async def update(self, wishlist_id: int, wishlist: Wishlist, db: AsyncSession):
        wishlist_db = await db.get(Wishlist, wishlist_id)
        if wishlist_db is None:
            return {"message": "Wishlist not found"}
        wishlist.modification_date = datetime.now()
        update_data = wishlist.__dict__
        update_data.pop("_sa_instance_state", None)
        update_data.pop("creation_date", None)
        update_data.pop("id", None)
        await db.execute(
            update(Wishlist).where(Wishlist.id == wishlist_id).values(**update_data)
        )
        await db.flush()
        await db.commit()
        return {"message": "Wishlist updated successfully"}

    async def delete(self, wishlist_id: int, db: AsyncSession):
        wishlist_db = await db.get(Wishlist, wishlist_id)
        if wishlist_db is None:
            return {"message": "Wishlist not found"}
        await db.delete(wishlist_db)
        await db.flush()
        await db.commit()
        return {"message": "Wishlist deleted successfully"}
