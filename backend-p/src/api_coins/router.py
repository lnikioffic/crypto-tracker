from fastapi import APIRouter
from src.api_coins.schemas import CoinName, CoinData
from src.api_coins.redis_client import RedisRepository
from src.api_coins.utils import CoinsResponse
from src.api_coins.utils import response_parser, dict_to_model_list

coin_router = APIRouter(prefix='/coins', tags=['Coins'])
redis_repository = RedisRepository()


@coin_router.get('/names', response_model=list[CoinName])
async def get_coins_list_name():
    coins = await redis_repository.get_coins()
    if coins:
        coins = dict_to_model_list(coins, CoinName)
        return coins

    coins_response = CoinsResponse()
    coins = await coins_response.get_coins_list()
    coins = response_parser(coins, CoinName)

    await redis_repository.set_coins(coins)
    return coins


@coin_router.get('/', response_model=list[CoinData])
async def get_coins_list():
    coins = await redis_repository.get_main_data()
    if coins:
        coins = dict_to_model_list(coins, CoinData)
        return coins

    coins_response = CoinsResponse()
    coins = await coins_response.get_coins_markets()
    coins = response_parser(coins, CoinData)

    await redis_repository.set_main_data(coins)
    return coins


@coin_router.get('/{id}')
async def get_coin():
    pass
