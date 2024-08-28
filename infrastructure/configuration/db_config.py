from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from infrastructure.settings.settings import settings

SQLALCHEMY_ASYNC_DATABASE_URL = settings.async_database_url

async_engine = create_async_engine(
    SQLALCHEMY_ASYNC_DATABASE_URL,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    pool_recycle=settings.pool_recycle,
    pool_timeout=settings.pool_timeout,
    echo_pool="debug",
    pool_pre_ping=True,
    pool_use_lifo=True,
    future=True,
    echo=True,
    isolation_level="READ COMMITTED"
)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


async def test_db_connection():
    async with async_engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
