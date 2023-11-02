import sqlalchemy as sa

from src.db.session import get_compyshopdb_session
from src.db.models import UserFavorites


async def add_product_to_favorites(
    user_id:int,
    product_id: int
) -> UserFavorites:
    """
    Update a product in the database by its ID.

    This function updates a product in the CompyShop database.
    It starts a new session and begins a transaction.
    Then it constructs a SQL UPDATE statement to update the product with the
    given ID and new values. The transaction is automatically committed at
    the end of the 'with' block.

    Args:
        product_id (int): The ID of the product to update.
        values (dict): A dictionary of column names and new values to update.

    Returns:
        None
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.insert(UserFavorites).values(
                user_id=user_id,
                product_id=product_id
            )
            insert_res = await s.execute(query)
            return insert_res.scalars().one_or_none()


async def delete_product_from_favorites(
    user_id: int,
    product_id: int
) -> bool:
    """
    Delete a product from a user's favorites.

    This function deletes a product from a user's favorites in the CompyShop database.
    It starts a new session and begins a transaction. Then it constructs a
    SQL DELETE statement to remove the product from the user's favorites.
    The transaction is automatically committed at the end of the 'with' block.

    Args:
        user_id (int): The ID of the user.
        product_id (int): The ID of the product to remove from the user's favorites.

    Returns:
        bool: True if the product was successfully removed, False otherwise.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.delete(UserFavorites).where(
                UserFavorites.user_id == user_id
            ).where(
                UserFavorites.product_id == product_id
            )
            delete_res = await s.execute(query)
            return True if delete_res.rowcount else False


async def get_all_favorites_ids(user_id: int) -> list[int]:
    """
    Get all product IDs from a user's favorites.

    This function retrieves all product IDs from a user's favorites in the
    CompyShop database. It starts a new session and begins a transaction.
    Then it constructs a SQL SELECT statement to get all product IDs from
    the user's favorites. The transaction is automatically committed at
    the end of the 'with' block.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list[int]: A list of product IDs from the user's favorites.
    """
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                UserFavorites.product_id
            ).where(
                UserFavorites.user_id == user_id
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()