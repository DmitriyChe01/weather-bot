import os
from dataclasses import dataclass, field
from functools import partial


@dataclass
class Setting:
    BOT_TOKEN: str = field(default_factory=partial(os.environ.get, 'BOT_TOKEN'))
    DB_DRIVER: str = field(default_factory=partial(os.environ.get, 'DB_DRIVER', 'postgresql+asyncpg'))
    DB_USER: str = field(default_factory=partial(os.environ.get, 'DB_USER', 'weather'))
    DB_PASS: str = field(default_factory=partial(os.environ.get, 'DB_PASS', '1234567890'))
    DB_HOST: int = field(default_factory=partial(os.environ.get, 'DB_HOST', 'db'))
    DB_PORT: int = field(default_factory=partial(os.environ.get, 'DB_PORT', '5432'))
    DB_NAME: str = field(default_factory=partial(os.environ.get, 'DB_NAME', 'weather'))

    REDIS_DRIVER: str = field(default_factory=partial(os.environ.get, 'REDIS_DRIVER', 'redis'))
    REDIS_HOST: str = field(default_factory=partial(os.environ.get, 'REDIS_HOST', 'redis'))
    REDIS_PORT: int = field(default_factory=partial(os.environ.get, 'REDIS_PORT', '6379'))

    @property
    def db_url(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def redis_url(self) -> str:
        return f'{self.REDIS_DRIVER}://{self.REDIS_HOST}:{self.REDIS_PORT}'


config = Setting()
