import json
import redis.asyncio as redis
from src.api_coins.schemas import Coin, CoinData
from src.api_coins.config import config_coins
from src.api_coins.utils import response_parser


class RedisRepository:
    def __init__(self):
        pool = redis.ConnectionPool.from_url(
            f'redis://{config_coins.REDIS_HOST}:{config_coins.REDIS_PORT}'
        )
        self._client = redis.Redis.from_pool(pool)

    async def set_coins(self, coins: list[Coin]):
        serialized = json.dumps([coin.model_dump() for coin in coins], default=str)
        await self._client.set("coins:list", serialized)

    async def get_coins(self) -> list[Coin]:
        data = await self._client.get("coins:list")
        if not data:
            return []
        coin_dicts = json.loads(data)
        return response_parser(coin_dicts, Coin)

    async def set_main_data(self, data: list[CoinData]):
        serialized = json.dumps([d.model_dump() for d in data], default=str)
        await self._client.set("coins:main_data", serialized)

    async def get_main_data(self) -> list[CoinData]:
        data = await self._client.get("coins:main_data")
        if not data:
            return []
        coin_dicts = json.loads(data)
        return response_parser(coin_dicts, CoinData)
