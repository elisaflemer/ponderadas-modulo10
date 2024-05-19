from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Security, Depends, Header
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"

def get_public_key():
    try:
        with open("./services/public_key.pem", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Public key not found")

def verify_token(token: str = Security()):
    public_key = get_public_key()
    try:
        decoded_token = jwt.decode(token, public_key, algorithms=["RS256"])
        return decoded_token  # Token is valid
    except InvalidTokenError as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Authorization scheme not supported")
    except ValueError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authorization header format.")
    
    # Verify the token using your verification function
    user_info = verify_token(token)
    if user_info is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    print(user_info)
    return user_info