import logging
from fastapi import FastAPI, APIRouter
from routers.produtos import router as produtos_router
from databases.database import get_session, engine, Base
import uvicorn
from logs.logs import log_info, log_error
app = FastAPI()

# Create API router with a prefix
api_router = APIRouter(prefix="/produtos")
api_router.include_router(produtos_router)

@app.on_event("startup")
async def startup():
    log_info("Iniciando aplicação")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log_info("Aplicação iniciada com sucesso")

@api_router.get("/heartbeat")
async def read_root():
    return {"message": "Produtos is alive!"}

# Include the API router
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)

