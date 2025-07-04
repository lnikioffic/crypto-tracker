from fastapi import APIRouter

portfolio_router = APIRouter(prefix='/portfolio', tags=['Portfolio'])


@portfolio_router.get('/')
async def get_portfolio():
    return {"message": "Portfolio endpoint is under construction."}
