
from fastapi import APIRouter, Depends
from schemas.usuarios import Usuarios as UsuarioSchema
from services.usuarios import UsuariosService
from databases.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from logs.logs import log_info, log_error

router = APIRouter()

@router.get("/{usuario_id}")
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /usuarios/{usuario_id}, método GET")
    usuariosService = UsuariosService()
    return await usuariosService.get(usuario_id, db)

@router.get("/")
async def get_usuarios(db:AsyncSession = Depends(get_session)):
    log_info("Acessando rota /usuarios, método GET")
    usuariosService = UsuariosService()
    return await usuariosService.get_all(db)

@router.post("/")
async def create_usuario(usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    log_info("Acessando rota /usuarios, método POST")
    usuariosService = UsuariosService()
    return await usuariosService.add(usuario=usuario, db=db)

@router.put("/{usuario_id}")
async def update_usuario(usuario_id: int, usuario: UsuarioSchema, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /usuarios/{usuario_id}, método PUT")
    usuariosService = UsuariosService()
    return await usuariosService.update(usuario_id, usuario=usuario, db=db)
    
@router.delete("/{usuario_id}")
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    log_info(f"Acessando rota /usuarios/{usuario_id}, método DELETE")
    usuariosService = UsuariosService()
    return await usuariosService.delete(usuario_id, db)
