import sqlalchemy as sa

from src.db.session import get_compyshopdb_session
from src.db.models import Catalogs, Products


async def delete_product_by_id(product_id: int) -> None:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.delete(
                Products
            ).where(
                Products.product_id == product_id
            )
            await s.execute(query)


async def delete_catalog_by_id(catalog_id: int) -> None:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            product_del_query = sa.delete(
                Products
            ).where(
                Products.catalog_id == catalog_id
            )
            await s.execute(product_del_query)

            catalog_del_query = sa.delete(
                Catalogs
            ).where(
                Catalogs.catalog_id == catalog_id
            )
            await s.execute(catalog_del_query)


async def add_catalog(title: str) -> list[Catalogs]:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.insert(
                Catalogs
            ).values(
                title=title
            )
            result = await s.execute(query)
            return result.scalar_one_or_none()


async def preapare_add_product(catalog_id: int) -> Products:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            insert_query = sa.insert(
                Products
            ).values(
                catalog_id=catalog_id,
                title='new_product',
                description='new_product',
                price=0
            )
            result = await s.execute(insert_query)
            
            select_query = sa.select(
                Products
            ).where(
                Products.title == 'new_product'
            )
            result = await s.execute(select_query)
            return result.scalar_one_or_none()


async def update_product(product_id: int, values: dict) -> None:
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.update(
                Products
            ).where(
                Products.product_id == product_id
            ).values(
                **values
            )
            await s.execute(query)
