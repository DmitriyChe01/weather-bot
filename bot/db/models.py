from sqlalchemy import Column, DateTime, BigInteger, Boolean, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from bot.db.base import Base
from datetime import datetime

city_telegram_user_table = Table(
    "city_telegram_user",
    Base.metadata,

    Column("city_id", ForeignKey("city.city_id")),
    Column("telegram_user_id", ForeignKey("telegram_user.user_id")),
    Column("datetime", DateTime, default=datetime.utcnow)
)


class TelegramUser(Base):
    __tablename__ = 'telegram_user'

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    is_bot = Column(Boolean, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    is_premium = Column(Boolean, nullable=True)
    city = relationship("City", secondary=city_telegram_user_table, back_populates="telegramUsers")


class City(Base):
    __tablename__ = 'city'

    city_id = Column(BigInteger, primary_key=True, unique=True)
    city_name = Column(String)
    telegramUsers = relationship("TelegramUser", secondary=city_telegram_user_table, back_populates="city")
