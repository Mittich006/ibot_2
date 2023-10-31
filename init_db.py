import asyncio

from asyncpg import connect as async_pg_connect

from src.db.session import CompyshopDBBase, compyshopdb_engine
from src.db.models import *
from src.config import settings
from src.logger import logger


# Database creation.
async def create_database():
    try:
        sys_conn = await async_pg_connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database='postgres'
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{settings.POSTGRES_HOST}" OWNER "{settings.POSTGRES_USER}"'
        )
        await sys_conn.execute(
            f'GRANT ALL PRIVILEGES ON DATABASE "{settings.POSTGRES_HOST}" TO "{settings.POSTGRES_USER}"'
        )
        logger.info("Database created")
    except Exception as e:
        logger.error("Failed to create database", error=e)
    else:
        await sys_conn.close()


# Tables creation from models.
async def create_tables():
    try:
        async with compyshopdb_engine.begin() as engine:
            await engine.run_sync(CompyshopDBBase.metadata.create_all)
        logger.info("Tables created")
    except Exception as e:
        logger.error("Failed to create database tables", error=e)
    else:
        await engine.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(create_database())
    loop.run_until_complete(create_tables())

    loop.close()