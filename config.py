from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Bot:
    token: str


@dataclass
class Config:
    bot: Bot


def load_config():
    return Config(
        bot=Bot(token=getenv("BOT_TOKEN")),
    )
