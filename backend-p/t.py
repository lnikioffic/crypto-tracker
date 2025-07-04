from src.api_coins.utils import CoinsResponse
import asyncio
from src.api_coins.redis_client import RedisRepository

redis = RedisRepository()


async def main():
    coi = await redis.get_coins()


async def cl():
    coins_response = CoinsResponse()
    coins = await coins_response.get_coins_list()
    await redis.set_main_data(coins)
    coins_from_redis = await redis.get_main_data()
    print(coins_from_redis)


asyncio.run(main())
