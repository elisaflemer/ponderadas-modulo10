from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import get_current_user
from database import get_session  # make sure to have this function defined in your database module
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from services.image_processor import convert_to_black_and_white
import io
import requests

router = APIRouter()

def get_service_access_token():
    file = open("./routes/service_token.txt", "r")
    return file.read()

@router.post("/black-and-white/")
async def process_image(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # Read the uploaded file
    image_data = await file.read()
    
    log = {
        "message": f"IMAGE UPLOADED: {file.filename}",
        "level": "INFO",
        "user_id": current_user["id"]
    }
    
    requests.post("http://localhost:8000/api/v1/logs/", json=log, headers={"Authorization": f"Bearer {get_service_access_token()}"})

    # Convert the image to black and white using the service function
    bw_image_data = await convert_to_black_and_white(image_data)
    
    

    # Return the processed image
    return StreamingResponse(io.BytesIO(bw_image_data), media_type="image/png")