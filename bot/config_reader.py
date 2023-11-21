from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    bot_token: SecretStr
    db_url: PostgresDsn
    redis_url: RedisDsn


config = Settings()
