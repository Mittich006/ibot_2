import sqlalchemy as sa

from src.db.session import get_compyshopdb_session
from src.db.models import UserFavorites


async def add_product_to_favorites(
    user_id:int,
    product_id: int
) -> UserFavorites:
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
    async with get_compyshopdb_session() as s:
        async with s.begin():
            query = sa.select(
                UserFavorites.product_id
            ).where(
                UserFavorites.user_id == user_id
            )
            select_res = await s.execute(query)
            return select_res.scalars().all()