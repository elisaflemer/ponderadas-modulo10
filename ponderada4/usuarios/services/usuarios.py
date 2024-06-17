# src/services/usuarios.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.usuarios import UsuariosRepository
from models.usuarios import Usuario
from schemas.usuarios import Usuarios as UsuariosSchema

class UsuariosService:
    def __init__(self):
        self.repository = UsuariosRepository()

    async def get(self, usuario_id, db: AsyncSession):
        usuario = await self.repository.get(usuario_id, db)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return usuario

    async def get_all(self, db: AsyncSession):
        return await self.repository.get_all(db)

    async def add(self, usuario : UsuariosSchema, db: AsyncSession):
        usuario = await Usuario(**usuario.dict(db))
        return self.repository.add(usuario)

    async def update(self, usuario_id, usuario : UsuariosSchema, db: AsyncSession):
        usuario = await Usuario(**usuario.dict())
        return self.repository.update(usuario_id, usuario, db)

    async def delete(self, usuario_id, db: AsyncSession):
        return await self.repository.delete(usuario_id, db)