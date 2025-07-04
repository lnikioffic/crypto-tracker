from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', case_sensitive=False, env_file_encoding='utf-8', extra='ignore'
    )


class ConfigDB(ConfigBase):
    HOST: str
    PORT: str
    USER: str
    PASSWORD: str
    DB: str

    model_config = SettingsConfigDict(
        env_prefix='POSTGRES_',
    )

    def get_db_url(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'


config_db = ConfigDB()
