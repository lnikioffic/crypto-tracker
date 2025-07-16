import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Path
from src.api_coins.schemas import CoinData, CurrencyEnum
from src.api_coins.utils import CoinsResponse, response_parser
from src.auth.dependencies import get_current_auth_user_by_token_sub
from src.auth.schemas import UserRead
from src.database import DbSession
from src.portfolio.schemas import (
    PortfolioCoinCreate,
    PortfolioCoinUpdate,
    PortfolioCreate,
    PortfolioRead,
    PortfolioUpdate,
)
from src.portfolio.service import (
    add_portfolio_coins,
    create_portfolio,
    delete_portfolio,
    delete_portfolio_coin,
    get_portfolio,
    get_portfolios,
    update_portfolio_attributes,
    update_portfolio_coins,
)

log = logging.getLogger(__name__)

portfolio_router = APIRouter(
    prefix='/portfolio',
    tags=['Portfolio'],
    dependencies=[Depends(get_current_auth_user_by_token_sub)],
)


@portfolio_router.get('/{id}', response_model=PortfolioRead)
async def get_portfolio_by_id(
    id: Annotated[int, Path],
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    session: DbSession,
    vs_currency: CurrencyEnum = CurrencyEnum.USD,
):
    coins_response = CoinsResponse()
    portfolio = await get_portfolio(session=session, portfolio_id=id, user_id=user.id)
    coins = await coins_response.get_coins_markets(
        vs_currency=vs_currency,
        params={'ids': ','.join(coin.coin_id for coin in portfolio.coins)},
    )
    coins_data: list[CoinData] = response_parser(coins, CoinData)

    portfolio = PortfolioRead.model_validate(portfolio, from_attributes=True)
    for coin_data in coins_data:
        for portfolio_coin in portfolio.coins:
            if portfolio_coin.coin_id == coin_data.id:
                portfolio_coin.total_value = (
                    coin_data.current_price * portfolio_coin.amount
                )
                portfolio.total_value += portfolio_coin.total_value
                portfolio_coin.coin_deatil = coin_data

    return portfolio


@portfolio_router.get('/', response_model=list[PortfolioRead])
async def get_portfolios_list(
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    session: DbSession,
    vs_currency: CurrencyEnum = CurrencyEnum.USD,
):
    coins_response = CoinsResponse()
    portfolios = await get_portfolios(session=session, user_id=user.id)

    coins = await coins_response.get_coins_markets(
        vs_currency=vs_currency,
        params={
            'ids': ','.join(
                coin.coin_id for portfolio in portfolios for coin in portfolio.coins
            )
        },
    )

    coins_data: list[CoinData] = response_parser(coins, CoinData)
    portfolios = [
        PortfolioRead.model_validate(portfolio, from_attributes=True)
        for portfolio in portfolios
    ]

    for portfolio in portfolios:
        for coin_data in coins_data:
            for portfolio_coin in portfolio.coins:
                if portfolio_coin.coin_id == coin_data.id:
                    portfolio_coin.total_value = (
                        coin_data.current_price * portfolio_coin.amount
                    )
                    portfolio.total_value += portfolio_coin.total_value
    return portfolios


@portfolio_router.post('/')
async def create_portfolio_handler(
    portfolio: PortfolioCreate,
    coins: list[PortfolioCoinCreate],
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    session: DbSession,
) -> dict:
    portfolio_new = await create_portfolio(
        session=session,
        portfolio_create=portfolio,
        coins=coins,
        user_id=user.id,
    )
    return {'id': portfolio_new.id}


@portfolio_router.delete('/{id}')
async def del_portfolio(
    id: Annotated[int, Path],
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    session: DbSession,
):
    check = await delete_portfolio(session=session, portfolio_id=id, user_id=user.id)
    if check:
        return {'message': 'портфель удалён'}

    log.error(f'Ошибка при удалении портфеля {id}, пользователя {user.id}')
    return {'message': 'Ошибка'}


@portfolio_router.patch('/{id}')
async def update_portfolio(
    session: DbSession,
    id: Annotated[int, Path],
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    update_data: PortfolioUpdate | None = None,
    new_coins: list[PortfolioCoinCreate] | None = None,
    update_coins: list[PortfolioCoinUpdate] | None = None,
):
    if update_data:
        await update_portfolio_attributes(
            session=session, portfolio_id=id, user_id=user.id, update_data=update_data
        )

    if update_coins:
        await update_portfolio_coins(
            session=session, portfolio_id=id, user_id=user.id, update_coins=update_coins
        )

    if new_coins:
        await add_portfolio_coins(
            session=session, portfolio_id=id, user_id=user.id, new_coins=new_coins
        )

    return {'message': 'Портфель обновлён'}


@portfolio_router.delete('/{portfolio_id}/{coin_id}')
async def delete_portfolio_coin_handler(
    coin_id: Annotated[int, Path],
    portfolio_id: Annotated[int, Path],
    user: Annotated[UserRead, Depends(get_current_auth_user_by_token_sub)],
    session: DbSession,
):
    check = await delete_portfolio_coin(
        session=session, coin_id=coin_id, portfolio_id=portfolio_id, user_id=user.id
    )
    if check:
        return {'message': 'монета удалена из портфеля'}

    log.error(
        f'Ошибка при удалении монеты из портфеля {portfolio_id}, монеты {coin_id}, пользователя {user.id}'
    )
    return {'message': 'Ошибка при удалении монеты из портфеля'}
