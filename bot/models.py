import asyncio
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, create_engine, MetaData, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from bot.config import DB_URL

Base = declarative_base()
metadata = MetaData()


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='alive')
    last_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    steps = Column(Integer, default=0)
    steps_updated_at = Column(DateTime, default=datetime.utcnow)


# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DB_URL, echo=False)

# Создаем асинхронный сеанс
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await init_db()

if __name__ == "__main__":
    asyncio.run(main())
