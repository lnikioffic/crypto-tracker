from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api_coins.redis_client import RedisRepository
from src.api_coins.router import coin_router
from src.auth.router import auth_router, user_router
from src.database import db
from src.portfolio.router import portfolio_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = RedisRepository()
    respons = await client._client.ping()
    print(f"Redis connection status: {respons}")
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware("http")
async def check_cookies(request: Request, call_next):
    # print("Cookies:", request.cookies)  # Для отладки
    response = await call_next(request)
    return response


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(coin_router)
app.include_router(portfolio_router)
