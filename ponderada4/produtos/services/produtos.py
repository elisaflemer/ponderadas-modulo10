# src/services/produtos.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.produtos import ProdutosRepository
from models.produtos import Produto
from schemas.produtos import Produto as ProdutosSchema

class ProdutosService:
    def __init__(self):
        self.repository = ProdutosRepository()

    async def get(self, produto_id, db: AsyncSession):
        produto = await self.repository.get(produto_id, db)
        if produto is None:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto

    async def get_all(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def add(self, produto : ProdutosSchema, db: AsyncSession):
        produto = await Produto(**produto.dict(db))
        return self.repository.add(produto)

    async def update(self, produto_id, produto : ProdutosSchema, db: AsyncSession):
        produto = await Produto(**produto.dict())
        return self.repository.update(produto_id, produto, db)

    async def delete(self, produto_id, db: AsyncSession):
        return await self.repository.delete(produto_id, db)