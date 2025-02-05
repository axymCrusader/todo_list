from typing import AsyncGenerator, Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import text
from datetime import datetime

from src.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    pool_size=5,
    max_overflow=10 
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession, 
    expire_on_commit=False
)


class Base(DeclarativeBase):
    @declared_attr
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

    updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )]
    


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

