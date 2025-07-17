import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status
from redis.exceptions import RedisError
from src.api_coins.redis_client import RedisRepository
from src.api_coins.schemas import CoinData, CoinName, CurrencyEnum
from src.api_coins.utils import CoinsResponse, response_parser

log = logging.getLogger(__name__)

coin_router = APIRouter(prefix='/coins', tags=['Coins'])
coins_response = CoinsResponse()


@coin_router.get('/names', status_code=200, response_model=list[CoinName])
async def get_coins_list_name():
    try:
        redis_repository = RedisRepository()
        coins = await redis_repository.get_coins()
        if coins:
            coins = [CoinName(**coin) for coin in coins]
            return coins
    except RedisError as ex:
        log.error(f'Redis unavailable: {ex}')

    coins = await coins_response.get_coins_list()
    coins = response_parser(coins, CoinName)

    try:
        await redis_repository.set_coins(coins)
    except RedisError as ex:
        log.error(f'Failed to cache data: {ex}')
    return coins


@coin_router.get('/', status_code=200, response_model=list[CoinData])
async def get_coins_list(
    vs_currency: CurrencyEnum = CurrencyEnum.USD,
):
    redis_repository = RedisRepository()
    try:
        coins = await redis_repository.get_main_data(key=vs_currency)
        if coins:
            coins = [CoinData(**coin) for coin in coins]
            return coins
    except RedisError as ex:
        log.error(f'Redis unavailable: {ex}')

    coins = await coins_response.get_coins_markets(vs_currency=vs_currency.value)
    coins = response_parser(coins, CoinData)

    try:
        await redis_repository.set_main_data(key=vs_currency, data=coins)
    except RedisError as ex:
        log.error(f'Failed to cache data: {ex}')

    return coins


@coin_router.get('/{ids}', status_code=200, response_model=CoinData)
async def get_coin(
    ids: Annotated[str, Path(description="Single CoinGecko id")],
    vs_currency: CurrencyEnum = CurrencyEnum.USD,
):
    if ',' in ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Only one id is allowed',
        )

    params = {'vs_currency': vs_currency, 'ids': ids}
    coins = await coins_response.get_coins_markets(
        vs_currency=vs_currency.value, params=params
    )
    coin = response_parser(coins, CoinData)
    if len(coin) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого токена нету',
        )
    return coin[0]
