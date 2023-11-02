import sqlalchemy as sa

from src.db.session import get_compyshopdb_session
from src.db.models import Catalogs, Products


async def get_all_catalogs() -> list[Catalogs]:
    """
    Get all catalogs from the database.

    This function gets all catalogs from the CompyShop database.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get all catalogs.
    The transaction is automatically committed at the end of the 'with' block.

    Returns:
        list[Catalogs]: A list of all catalogs in the database.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Catalogs
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()


async def get_catalog_id_by_title(catalog_title: str) -> int:
    """
    Get a catalog's ID from the database by its title.

    This function gets a catalog's ID from the CompyShop database by its title.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get the catalog's ID.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        catalog_title (str): The title of the catalog to get the ID of.

    Returns:
        int: The ID of the catalog with the given title.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Catalogs.catalog_id
            ).where(
                Catalogs.title == catalog_title
            )
            select_res = await s.execute(query)
            return select_res.scalar_one_or_none()


async def get_catalog_title_by_id(catalog_id: int) -> str:
    """
    Get a catalog's title from the database by its ID.

    This function gets a catalog's title from the CompyShop database by its ID.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get the catalog's title.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        catalog_id (int): The ID of the catalog to get the title of.

    Returns:
        str: The title of the catalog with the given ID.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Catalogs.title
            ).where(
                Catalogs.catalog_id == catalog_id
            )
            select_res = await s.execute(query)
            return select_res.scalar_one_or_none()


async def get_all_products_by_catalog(catalog_id: int) -> tuple[Products]:
    """
    Get all products in a catalog from the database.

    This function gets all products in a catalog from the CompyShop database.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get all products in the catalog.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        catalog_id (int): The ID of the catalog to get the products of.

    Returns:
        tuple[Products]: A tuple of all products in the catalog with the given ID.
    """
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
    """
    Get a product from the database by its ID.

    This function gets a product from the CompyShop database by its ID.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get the product.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        product_id (int): The ID of the product to get.

    Returns:
        Products: The product with the given ID.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Products
            ).where(
                Products.product_id == product_id
            )
            select_res = await s.execute(query)
            return select_res.scalar_one_or_none()


async def get_all_products_by_ids(product_ids: list[int]) -> tuple[Products]:
    """
    Get all products from the database by their IDs.

    This function gets all products from the CompyShop database by their IDs.
    It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get the products.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        product_ids (list[int]): A list of IDs of the products to get.

    Returns:
        tuple[Products]: A tuple of all products with the given IDs.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                Products
            ).where(
                Products.product_id.in_(product_ids)
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()