from datetime import datetime

from pydantic import BaseModel


class CoinName(BaseModel):
    id: str
    name: str

class Coin(BaseModel):
    id: str
    symbol: str
    name: str
    platforms: dict[str, str]


class CoinData(BaseModel):
    id: str
    symbol: str
    name: str
    image: str
    current_price: float
    market_cap: float
    market_cap_rank: int
    fully_diluted_valuation: float
    total_volume: float
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    circulating_supply: float
    total_supply: float
    max_supply: float | None = None
    last_updated: datetime
