# routers/produtos.py

from fastapi import APIRouter, Depends
from schemas.produtos import Produto as ProdutoSchema
from services.produtos import ProdutosService
from databases.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from logs.logs import log_info, log_error

router = APIRouter()

@router.get("/{produtos_id}")
async def get_produtos(produtos_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /produtos/{produtos_id}, método GET")
    produtosService = ProdutosService()
    return await produtosService.get(produtos_id, db)

@router.get("/")
async def get_produtoss(db:AsyncSession = Depends(get_session)):
    log_info("Acessando rota /produtos, método GET")
    produtosService = ProdutosService()
    return await produtosService.get_all(db)

@router.post("/")
async def create_produtos(produtos: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    log_info("Acessando rota /produtos, método POST")
    produtosService = ProdutosService()
    return await produtosService.add(produtos=produtos, db=db)

@router.put("/{produtos_id}")
async def update_produtos(produtos_id: int, produtos: ProdutoSchema, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /produtos/{produtos_id}, método PUT")
    produtosService = ProdutosService()
    return await produtosService.update(produtos_id, produtos=produtos, db=db)
    
@router.delete("/{produtos_id}")
async def delete_produtos(produtos_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /produtos/{produtos_id}, método DELETE")
    produtosService = ProdutosService()
    return await produtosService.delete(produtos_id, db)
