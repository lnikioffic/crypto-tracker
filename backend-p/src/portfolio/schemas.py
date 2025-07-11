from pydantic import BaseModel, ConfigDict


class PortfolioCoinBase(BaseModel):
    coin_id: str
    amount: float


class PortfolioCoinRead(PortfolioCoinBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


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


class PortfolioCreate(PortfolioBase):
    pass


class PortfolioUpdate(BaseModel):
    name: str | None = None


# Для PATCH-запроса с обновлением монет и добавлением новых
class PortfolioPatch(BaseModel):
    name: str | None = None
    new_coins: list[PortfolioCoinCreate] | None = None
    update_coins: list[PortfolioCoinUpdate] | None = None
