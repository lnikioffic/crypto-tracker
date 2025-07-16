import httpx
from pydantic import BaseModel
from src.api_coins.config import config_coins
from src.api_coins.schemas import CurrencyEnum


class HttpClient:
    def __init__(self, base_url: str, headers: dict[str, str]):
        self._base_url = base_url
        self._headers = headers

    async def get_respons(
        self, url: str, params: dict[str, str] | None = None
    ) -> httpx.Response:
        async with httpx.AsyncClient(
            base_url=self._base_url, headers=self._headers, params=params
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
        return response


def response_parser[T: BaseModel](response: httpx.Response, type_pars: T) -> list[T]:
    if response.status_code != 200:
        raise ValueError(f'Error: {response.status_code}')

    return [type_pars(**item) for item in response.json()]


class CoinsResponse:
    def __init__(self):
        self._base_url = 'https://api.coingecko.com'
        self._headers = {
            'accept': 'application/json',
            'x-cg-demo-api-key': config_coins.API_KEY,
        }
        self._client = HttpClient(self._base_url, self._headers)

    async def get_coins_list(self) -> httpx.Response:
        params = {'include_platform': 'true'}
        url = '/api/v3/coins/list'
        response = await self._client.get_respons(url, params)
        return response

    async def get_coins_markets(
        self,
        vs_currency: CurrencyEnum = CurrencyEnum.USD,
        params: dict[str, str] | None = None,
    ) -> httpx.Response:
        default_params = {'vs_currency': vs_currency}
        if params is None:
            params = default_params
        else:
            params.update(default_params)
        url = '/api/v3/coins/markets'
        response = await self._client.get_respons(url, params)
        return response
