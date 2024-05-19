from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from database import get_session, engine, Base
import uvicorn
import logging
from routes.users import router

logging.basicConfig()    
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

app = FastAPI()
api_router = APIRouter(prefix="/api/v1/users")
api_router.include_router(router)

@api_router.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)