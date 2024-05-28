from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import get_current_user
from database import get_session  # make sure to have this function defined in your database module
from services.logs import create_log, get_all_logs
from fastapi import APIRouter, File, UploadFile
import io
from models.schema import LogSchema

router = APIRouter()

@router.post("/")
async def add_log(log: LogSchema, session: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    print(log)
    return await create_log(session, log.message, log.level, current_user['sub'])

@router.get("/")
async def get_logs(session: AsyncSession = Depends(get_session)):
    return await get_all_logs(session)