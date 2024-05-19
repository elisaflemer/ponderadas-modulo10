from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import get_current_user
from database import get_session  # make sure to have this function defined in your database module
from services.logs import create_log

router = APIRouter()

@router.post("/process")
async def process_image(session: AsyncSession = Depends(get_session), user = Depends(get_current_user)):
    create_log(session, f"IMAGE PROCESSING REQUESTED", user_id=user['id'])
    return {"message": "Image processing completed"}