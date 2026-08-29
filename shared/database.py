"""
Database utilities for service initialization.
"""

from sqlalchemy import create_engine, pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator, Optional

Base = declarative_base()


def get_engine(database_url: str, echo: bool = False):
    """Create SQLAlchemy engine with connection pooling."""
    if database_url.startswith("postgresql+asyncpg://"):
        # Async engine for async operations
        return create_async_engine(
            database_url,
            echo=echo,
            poolclass=pool.NullPool,  # Use NullPool to avoid connection issues
            connect_args={"server_settings": {"application_name": "shopzy"}},
        )
    else:
        # Synchronous engine
        return create_engine(
            database_url,
            echo=echo,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,  # Verify connections before using
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {},
        )


def get_session_factory(engine):
    """Create session factory."""
    if hasattr(engine, "aclose"):
        # Async engine
        return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    else:
        # Sync engine
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db_session(session_factory) -> AsyncGenerator[AsyncSession, None]:
    """Async generator for database sessions."""
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
