from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import get_current_user
from database import get_session  # make sure to have this function defined in your database module
from services.logs import create_log
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from services.image_processor import convert_to_black_and_white
import io

router = APIRouter()

@router.post("/black-and-white/")
async def process_image(file: UploadFile = File(...)):
    # Read the uploaded file
    print(file.filename)
    image_data = await file.read()

    # Convert the image to black and white using the service function
    bw_image_data = await convert_to_black_and_white(image_data)

    # Return the processed image
    return StreamingResponse(io.BytesIO(bw_image_data), media_type="image/png")