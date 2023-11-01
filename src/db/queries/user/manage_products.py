import sqlalchemy as sa
from aiogram.types import Message

from src.db.session import get_compyshopdb_session
from src.db.models import Catalogs, Products


async def get_all_catalogs() -> list[Catalogs]:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Catalogs
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()


async def get_catalog_id_by_title(catalog_title: str) -> int:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Catalogs.catalog_id
            ).where(
                Catalogs.title == catalog_title
            )
            select_res = await s.execute(query)
            return select_res.scalar_one_or_none()


async def get_all_products_by_catalog(catalog_id: int) -> tuple[Products]:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Products
            ).where(
                Products.catalog_id == catalog_id
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()


async def get_product_by_id(product_id: int) -> Products:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Products
            ).where(
                Products.product_id == product_id
            )
            select_res = await s.execute(query)
            return select_res.scalar_one_or_none()