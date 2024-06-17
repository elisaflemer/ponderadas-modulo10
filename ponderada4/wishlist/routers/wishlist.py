# routers/wishlist.py

from fastapi import APIRouter, Depends
from schemas.wishlist import Wishlist as WishlistSchema
from services.wishlist import WishlistService
from databases.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/{wishlist_id}")
async def get_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService()
    return await wishlistService.get(wishlist_id, db)

@router.get("/")
async def get_wishlists(db:AsyncSession = Depends(get_session)):
    wishlistService = WishlistService()
    return await wishlistService.get_all(db)

@router.post("/")
async def create_wishlist(wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService()
    return await wishlistService.add(wishlist, db)

@router.put("/{wishlist_id}")
async def update_wishlist(wishlist_id: int, wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService()
    return await wishlistService.update(wishlist_id,wishlist, db)
    
@router.delete("/{wishlist_id}")
async def delete_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService()
    return await wishlistService.delete(wishlist_id, db)
