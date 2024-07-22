from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app import config

engine = create_async_engine(config.SQLALCHEMY_DB_URL, echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

async def async_create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def async_drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)