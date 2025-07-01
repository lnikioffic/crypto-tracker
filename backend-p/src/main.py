from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.auth.router import auth_router, user_router
from src.database import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
