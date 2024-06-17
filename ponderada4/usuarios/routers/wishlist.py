# routers/wishlist.py

from fastapi import APIRouter, Depends
from schemas.wishlist import Wishlist as WishlistSchema
from services.wishlist import WishlistService
from databases import database


router = APIRouter()

@router.get("/wishlist/{wishlist_id}")
async def get_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService(db)
    return await wishlistService.get(wishlist_id)

@router.get("/wishlist")
async def get_wishlists(db:AsyncSession = Depends(get_session)):
    wishlistService = WishlistService(db)
    return await wishlistService.get_all()

@router.post("/wishlist")
async def create_wishlist(wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService(db)
    return await wishlistService.add(wishlist=wishlist)

@router.put("/wishlist/{wishlist_id}")
async def update_wishlist(wishlist_id: int, wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService(db)
    return await wishlistService.update(wishlist_id, wishlist=wishlist)
    
@router.delete("/wishlist/{wishlist_id}")
async def delete_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    wishlistService = WishlistService(db)
    return await wishlistService.delete(wishlist_id)
