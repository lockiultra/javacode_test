from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.v1.core.settings import settings
from api.v1.models.wallet import Wallet # noqa


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    echo=False,
    future=True
)
sessionlocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        await session.close()
