from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import get_current_user
from database import get_session  # make sure to have this function defined in your database module
from services.logs import create_log
from fastapi import APIRouter, File, UploadFile
import io

router = APIRouter()

@router.post("/")
async def add_log(log: dict, session: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    return await create_log(session, log)

@router.get("/")
async def get_logs(session: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
    return await get_logs(session)