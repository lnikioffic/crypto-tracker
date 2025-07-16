import json

import redis.asyncio as redis
from src.api_coins.config import config_coins
from src.api_coins.schemas import Coin, CoinData


class RedisRepository:
    def __init__(self):
        pool = redis.ConnectionPool.from_url(
            f'redis://{config_coins.REDIS_HOST}:{config_coins.REDIS_PORT}'
        )
        self._client = redis.Redis.from_pool(pool)

    async def set_coins(self, coins: list[Coin]):
        serialized = json.dumps([coin.model_dump() for coin in coins], default=str)
        await self._client.set('coins:list', serialized, ex=3600)  # 1 hour expiration

    async def get_coins(self) -> list[dict]:
        data = await self._client.get('coins:list')
        if not data:
            return []
        coin_dicts = json.loads(data)
        return coin_dicts

    async def set_main_data(self, key: str, data: list[CoinData]):
        serialized = json.dumps([d.model_dump() for d in data], default=str)
        await self._client.set(
            f'coins:main_data:{key}', serialized, ex=120
        )  # 2 minutes expiration

    async def get_main_data(self, key: str) -> list[dict]:
        data = await self._client.get(f'coins:main_data{key}')
        if not data:
            return []
        coin_dicts = json.loads(data)
        return coin_dicts
