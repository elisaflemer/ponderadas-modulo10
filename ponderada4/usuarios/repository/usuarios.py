# src/repository/usuarios.py

from models.usuarios import Usuario
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.sql import select, update
from datetime import datetime
from schemas.usuarios import Usuarios as UsuariosSchema

class UsuariosRepository:
    def __init__(self):
        pass

    async def get(self, usuarios_id: int, db: AsyncSession):
        stmt = select(Usuario).where(Usuario.id == usuarios_id)
        result = await db.execute(stmt)
        result = result.scalars().first()
        return result
    
    async def get_all(self, db: AsyncSession):
        stmt = select(Usuario)
        result = await db.execute(stmt)
        result = result.scalars().all()
        return

    async def add(self, usuarios: Usuario, db: AsyncSession):
        usuarios.created_at = datetime.now()
        db.add(usuarios)
        await db.commit()
        return usuarios

    async def update(self, usuarios_id: int, usuarios: UsuariosSchema, db: AsyncSession):
        usuarios_db = await db.get(Usuario, usuarios_id)
        if usuarios_db is None:
            return {"message": "Usuario não encontrado"}
        usuarios_db.id_cliente = usuarios.id_cliente
        usuarios_db.id_produto = usuarios.id_produto
        await db.commit()
        return usuarios_db

    async def delete(self, usuarios_id: int, db: AsyncSession):
        usuarios = await db.get(Usuario, usuarios_id)
        if usuarios is None:
            return {"message": "Usuario não encontrado"}
        db.delete(usuarios)
        await db.commit()
        return {"message": "Usuario deletado"}