# routers/produtos.py

from fastapi import APIRouter, Depends
from schemas.produtos import Produto as ProdutoSchema
from services.produtos import ProdutosService
from databases.databse import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/{produtos_id}")
async def get_produtos(produtos_id: int, db: AsyncSession = Depends(get_session)):
    produtosService = ProdutosService(db)
    return await produtosService.get(produtos_id)

@router.get("/")
async def get_produtoss(db:AsyncSession = Depends(get_session)):
    produtosService = ProdutosService(db)
    return await produtosService.get_all()

@router.post("/")
async def create_produtos(produtos: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    produtosService = ProdutosService(db)
    return await produtosService.add(produtos=produtos)

@router.put("/{produtos_id}")
async def update_produtos(produtos_id: int, produtos: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    produtosService = ProdutosService(db)
    return await produtosService.update(produtos_id, produtos=produtos)
    
@router.delete("/{produtos_id}")
async def delete_produtos(produtos_id: int, db: AsyncSession = Depends(get_session)):
    produtosService = ProdutosService(db)
    return await produtosService.delete(produtos_id)
