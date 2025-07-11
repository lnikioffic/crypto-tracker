import asyncio

from src.api_coins.schemas import Coin
from src.api_coins.utils import CoinsResponse, response_parser


async def main():
    pass


async def cl():
    coins_response = CoinsResponse()
    coins = await coins_response.get_coins_list()
    coins = response_parser(coins, Coin)
    print(coins)


asyncio.run(cl())
