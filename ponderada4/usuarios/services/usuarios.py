# src/services/usuarios.py

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from repository.usuarios import UsuariosRepository
from models.usuarios import Usuario
from schemas.usuarios import Usuarios as UsuariosSchema
from logs.logs import log_info, log_error, log_warning

class UsuariosService:
    def __init__(self):
        self.repository = UsuariosRepository()

    async def get(self, usuario_id, db: AsyncSession):
        usuario = await self.repository.get(usuario_id, db)
        if usuario is None:
            log_error("Usuario não encontrado")
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return usuario

    async def get_all(self, db: AsyncSession):
        usuarios = await self.repository.get_all(db)
        if not usuarios:
            log_warning("Nenhum usuario encontrado")
            raise HTTPException(status_code=404, detail="Nenhum usuario encontrado")
        return usuarios

    async def add(self, usuario : UsuariosSchema, db: AsyncSession):
        usuario = await Usuario(**usuario.dict(db))
        return self.repository.add(usuario)

    async def update(self, usuario_id, usuario : UsuariosSchema, db: AsyncSession):
        usuario = await Usuario(**usuario.dict())
        return self.repository.update(usuario_id, usuario, db)

    async def delete(self, usuario_id, db: AsyncSession):
        usuario = await self.repository.get(usuario_id, db)
        if usuario is None:
            log_error("Usuario não encontrado")
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        return await self.repository.delete(usuario_id, db)