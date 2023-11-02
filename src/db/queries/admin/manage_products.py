import sqlalchemy as sa

from src.db.session import get_compyshopdb_session
from src.db.models import Catalogs, Products


async def delete_product_by_id(product_id: int) -> None:
    """
    Delete a product from the database by its ID.

    This function deletes a product from the CompyShop database.
    It starts a new session and begins a transaction.
    Then it constructs a SQL DELETE statement to delete the product with the given ID.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        product_id (int): The ID of the product to delete.

    Returns:
        None
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.delete(
                Products
            ).where(
                Products.product_id == product_id
            )
            await s.execute(query)


async def delete_catalog_by_id(catalog_id: int) -> None:
    """
    Delete a catalog and its associated products from the database by its ID.

    This function deletes a catalog and all products associated with it from
    the CompyShop database. 
    It starts a new session and begins a transaction. Then it constructs SQL DELETE statements to delete the products and the catalog with the given ID.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        catalog_id (int): The ID of the catalog to delete.

    Returns:
        None
    """
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
    """
    Add a new catalog to the database.

    This function adds a new catalog to the CompyShop database.
    It starts a new session and begins a transaction. Then it constructs a SQL INSERT statement to add the catalog with the given title. The transaction is automatically committed at the end of the 'with' block.

    Args:
        title (str): The title of the catalog to add.

    Returns:
        list[Catalogs]: The newly added catalog object.
    """
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
    """
    Prepare a new product to be added to a specific catalog in the database.

    This function prepares a new product with default values to be added to
    a specific catalog in the CompyShop database. It starts a new session and
    begins a transaction. Then it constructs a SQL INSERT statement to
    add the product with the given catalog_id. After the product is added, 
    it selects the product back from the database to return.

    Args:
        catalog_id (int): The ID of the catalog to which the product will be added.

    Returns:
        Products: The newly added product object.
    """
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
    """
    Update a product in the database by its ID.

    This function updates a product in the CompyShop database. It starts a
    new session and begins a transaction. Then it constructs a SQL UPDATE
    statement to update the product with the given ID and new values.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        product_id (int): The ID of the product to update.
        values (dict): A dictionary of column names and new values to update.

    Returns:
        None
    """
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
