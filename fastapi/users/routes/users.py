from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth import hash_password, create_access_token, verify_password
from services.users import get_users, get_user_by_email, get_user_by_id, create_user
from database import get_session  # make sure to have this function defined in your database module
from models.schemas import UserRegistrationRequest, UserResponseModel, LoginResponseModel, UserLoginRequest
import requests
import os
import json

router = APIRouter()

def get_service_access_token():
    file = open("./routes/service_token.txt", "r")
    return file.read()

service_access_token = get_service_access_token()

@router.post("/register", response_model=UserResponseModel)  
async def register(request: UserRegistrationRequest, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, request.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = hash_password(request.password)
    user = await create_user(session, request.email, hashed_password)
    # send request to log microservice
    log = {
        "message": f"NEW USER REGISTERED: {user.email}",
        "level": "INFO",
        "user": user.email
    }
    requests.post(f"{os.getenv('GATEWAY_URL')}/api/v1/logs/", json=log, headers={"Authorization": f"Bearer {service_access_token}", "Content-Type": "application/json"})
    return UserResponseModel(id=user.id, email=user.email)

@router.post("/login", response_model=LoginResponseModel)
async def login(request: UserLoginRequest, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, request.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = create_access_token(data={"sub": user.email})
    
    # send request to log microservice
    log = {
        "message": f"USER LOGGED IN: {user.email}",
        "level": "INFO",
        "user": user.email
    }
    
    requests.post(f"{os.getenv('GATEWAY_URL')}/api/v1/logs/", json=log, headers={"Authorization": f"Bearer {service_access_token}", "Content-Type": "application/json"})
    
    return LoginResponseModel(email=user.email, access_token=access_token, token_type="bearer")

@router.get("/users/{user_email}", response_model=UserResponseModel)
async def get_user(user_email: str, session: AsyncSession = Depends(get_session)):
    user = await get_user_by_email(session, user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponseModel(id=user.id, email=user.email)

