from pydantic_settings import SettingsConfigDict
from src.config import ConfigBase


class ConfigCoins(ConfigBase):
    API_KEY: str
    REDIS_HOST: str
    REDIS_PORT: str

    model_config = SettingsConfigDict(
        env_prefix='COINS_',
    )


config_coins = ConfigCoins()
