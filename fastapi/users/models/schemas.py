from pydantic import BaseModel
import enum

class UserRegistrationRequest(BaseModel):
    email: str
    password: str

class UserResponseModel(BaseModel):
    id: int
    email: str

class LoginResponseModel(BaseModel):
    email: str
    access_token: str
    token_type: str

class UserLoginRequest(BaseModel):
    email: str
    password: str