from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import (
    select,
    insert,
    delete,
    update
)

from src.config import settings


# Create a base class for declarative models bound to the PostgreSQL CompyshopDB engine
class CompyshopDBBase(DeclarativeBase):
    pass


# Create an async engine for the PostgreSQL CompyshopDB
compyshopdb_engine = create_async_engine(
    settings.COMPYSHOPDB_URL,
    pool_pre_ping=True,
    future=True
)


@asynccontextmanager
async def get_compyshopdb_session() -> AsyncIterator[AsyncSession]:
    """
    Create a context manager for an asynchronous database session to the PostgreSQL CompyshopDB.

    Yields:
        session: An asynchronous SQLAlchemy session for the PostgreSQL CompyshopDB.

    This function is an async context manager that provides a session to interact with
    the PostgreSQL TechnicalDB. It automatically handles setup and teardown by using the
    sessionmaker to create a session and closing the session when the context is exited.

    Example usage:

        async with get_compyshopdb_session() as session:
            # Interact with the session here.
            result = await session.execute(query)
            data = result.fetchall()

    When the `with` block is exited, the session is automatically closed.
    """
    # Create a sessionmaker for the PostgreSQL TechnicalDB engine
    compyshopdb_session = sessionmaker(
        bind=compyshopdb_engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession
    )

    # Open the session and yield it to the caller
    async with compyshopdb_session() as session:
        yield session
        await compyshopdb_engine.dispose()