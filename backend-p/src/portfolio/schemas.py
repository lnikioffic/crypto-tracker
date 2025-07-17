from pydantic import BaseModel, ConfigDict, Field
from src.api_coins.schemas import CoinData


class PortfolioCoinBase(BaseModel):
    coin_id: str
    amount: float = Field(gt=0)


class PortfolioCoinRead(PortfolioCoinBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    total_value: float | None = None

    coin_deatil: CoinData | None = None


class PortfolioCoinCreate(PortfolioCoinBase):
    pass


class PortfolioCoinUpdate(BaseModel):
    id: int
    amount: float


class PortfolioBase(BaseModel):
    name: str


class PortfolioRead(PortfolioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    coins: list[PortfolioCoinRead]

    total_value: float = Field(default=0.0)


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = None


# Для PATCH-запроса с обновлением монет и добавлением новых
class PortfolioPatch(BaseModel):
    name: str | None = None
    new_coins: list[PortfolioCoinCreate] | None = None
    update_coins: list[PortfolioCoinUpdate] | None = None
