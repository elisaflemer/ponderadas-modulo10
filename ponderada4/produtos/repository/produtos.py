
from models.produtos import Produto
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select, update
from datetime import datetime
from schemas.produtos import Produto as ProdutosSchema

class ProdutosRepository:
    def __init__(self):
        pass

    async def get(self, produto_id: int, db: AsyncSession):
        stmt = select(Produto).where(Produto.id == produto_id)
        result = await db.execute(stmt)
        result = result.scalars().first()
        return result
    
    async def get_all(self, db: AsyncSession):
        stmt = select(Produto)
        result = await db.execute(stmt)
        result = result.scalars().all()
        return

    async def add(self, produto: Produto, db: AsyncSession):
        produto.created_at = datetime.now()
        db.add(produto)
        await db.commit()
        return produto

    async def update(self, produto_id: int, produto: ProdutosSchema, db: AsyncSession):
        produto_db = await db.get(Produto, produto_id)
        if produto_db is None:
            return {"message": "Produto não encontrado"}
        produto_db.id_cliente = produto.id_cliente
        produto_db.id_produto = produto.id_produto
        await db.commit()
        return produto_db

    async def delete(self, produto_id: int, db: AsyncSession):
        produto = await db.get(Produto, produto_id)
        if produto is None:
            return {"message": "Produto não encontrado"}
        db.delete(produto)
        await db.commit()
        return {"message": "Produto deletado"}