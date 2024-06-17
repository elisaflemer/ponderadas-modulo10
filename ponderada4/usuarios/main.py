import logging
from fastapi import FastAPI, APIRouter
from routers.usuarios import router as usuarios_router
from databases.database import get_session, engine, Base
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Create API router with a prefix
api_router = APIRouter(prefix="/usuarios")
api_router.include_router(usuarios_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@api_router.get("/heartbeat")
async def read_root():
    return {"message": "Usuarios is alive!"}

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

