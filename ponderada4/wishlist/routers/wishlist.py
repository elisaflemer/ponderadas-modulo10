# routers/wishlist.py

from fastapi import APIRouter, Depends
from schemas.wishlist import Wishlist as WishlistSchema
from services.wishlist import WishlistService
from databases.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from logs.logs import log_info, log_error

router = APIRouter()

@router.get("/{wishlist_id}")
async def get_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /wishlist/{wishlist_id}, método GET")
    wishlistService = WishlistService()
    return await wishlistService.get(wishlist_id, db)

@router.get("/")

async def get_wishlists(db:AsyncSession = Depends(get_session)):
    log_info("Acessando rota /wishlist, método GET")
    wishlistService = WishlistService()
    return await wishlistService.get_all(db)

@router.post("/")
async def create_wishlist(wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    log_info("Acessando rota /wishlist, método POST")
    wishlistService = WishlistService()
    return await wishlistService.add(wishlist, db)

@router.put("/{wishlist_id}")
async def update_wishlist(wishlist_id: int, wishlist: WishlistSchema, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /wishlist/{wishlist_id}, método PUT")
    wishlistService = WishlistService()
    return await wishlistService.update(wishlist_id,wishlist, db)
    
@router.delete("/{wishlist_id}")
async def delete_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /wishlist/{wishlist_id}, método DELETE")
    wishlistService = WishlistService()
    return await wishlistService.delete(wishlist_id, db)
