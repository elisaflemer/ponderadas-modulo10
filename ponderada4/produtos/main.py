import logging
import json
import sys
import traceback

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from fastapi import FastAPI, APIRouter, Depends
    from routers.wishlist import router as wishlist_router
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.future import select
    from databases.database import get_session, engine, Base
    import uvicorn
    from models.wishlist import Wishlist

    # Initialize FastAPI app
    app = FastAPI()

    # Create API router with a prefix
    api_router = APIRouter(prefix="/wishlist")
    api_router.include_router(wishlist_router)

    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @api_router.get("/heartbeat")
    async def read_root():
        return {"message": "Wishlist is alive!"}

    # Include the API router
    app.include_router(api_router)

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError as e:
    error_info = {
        "error": str(e),
        "type": type(e).__name__,
        "traceback": traceback.format_exc().splitlines()
    }
    logger.error(json.dumps(error_info))
    sys.exit(1)
