
from fastapi import APIRouter, Depends
from schemas.usuarios import Usuarios as UsuarioSchema
from services.usuarios import UsuariosService
from databases.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get("/{usuario_id}")
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuariosService = UsuariosService(db)
    return await usuariosService.get(usuario_id)

@router.get("/")
async def get_usuarios(db:AsyncSession = Depends(get_session)):
    usuariosService = UsuariosService(db)
    return await usuariosService.get_all()

@router.post("/")
async def create_usuario(usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    usuariosService = UsuariosService(db)
    return await usuariosService.add(usuario=usuario)

@router.put("/{usuario_id}")
async def update_usuario(usuario_id: int, usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    usuariosService = UsuariosService(db)
    return await usuariosService.update(usuario_id, usuario=usuario)
    
@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    usuariosService = UsuariosService(db)
    return await usuariosService.delete(usuario_id)
