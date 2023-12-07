from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.dev', '.env.prod'), env_file_encoding='utf-8',
                                      extra='ignore')
    bot_token: SecretStr
    DB_DRIVER: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    REDIS_DRIVER: str
    REDIS_HOST: str
    REDIS_PORT: int

    NGINX_HOST: str

    @property
    def db_url(self) -> PostgresDsn:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def redis_url(self) -> RedisDsn:
        return f'{self.REDIS_DRIVER}://{self.REDIS_HOST}:{self.REDIS_PORT}'


config = Settings()
