import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.api_coins.redis_client import RedisRepository
from src.api_coins.router import coin_router
from src.auth.router import auth_router, user_router
from src.database import db
from src.logging import configure_logging
from src.portfolio.router import portfolio_router

log = logging.getLogger(__name__)
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = RedisRepository()
    response = await client._client.ping()
    print(f"Redis connection status: {response}")
    log.info(f"Redis connection status: {response}")
    log.error(' Application startup failed. Exiting.', exc_info=True)
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
    
    log.info(f"Request started: {request.method} {request.url}")
    response = await call_next(request)
    log.info(
        f'Request completed: {request.method} {request.url} - Status: {response.status_code}'
    )
    return response


app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(coin_router)
app.include_router(portfolio_router)
