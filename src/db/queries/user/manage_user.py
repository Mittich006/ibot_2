import sqlalchemy as sa
from aiogram.types import Message

from src.db.session import get_compyshopdb_session
from src.db.models import Users


async def get_or_create_user(message: Message) -> Users:
    '''
    Get user from database by `aiogram.types.Message`.
    If user not found, create new user.


    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        models.Users: User from database.
    '''
    async with get_compyshopdb_session() as s:
        async with s.begin():

            if message.from_user.is_bot:
                values = {
                    'identity_id': str(message.chat.id),
                    'username': message.chat.username or None,
                    'first_name': message.chat.first_name,
                    'last_name': message.chat.last_name or None,
                }
            else:
                values = {
                    'identity_id': str(message.from_user.id),
                    'username': message.from_user.username or None,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name or None,
                }

            select_query = sa.select(
                Users
            ).filter_by(
                identity_id=str(values.get('identity_id'))
            )
            select_res = await s.execute(select_query)

            if not select_res.scalar_one_or_none():
                query = sa.insert(
                    Users
                ).values(
                    values
                )
                await s.execute(query)

            select_res = await s.execute(select_query)
            return select_res.scalar_one_or_none()


async def get_user(message: Message) -> Users:
    '''
    Get user from database by `aiogram.types.Message`.
    If user not found, return None.


    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        models.Users: User from database.
    '''
    async with get_compyshopdb_session() as s:
        async with s.begin():
            if message.from_user.is_bot:
                identity_id = message.chat.id
            else:
                identity_id = message.from_user.id

            select_query = sa.select(
                Users
            ).filter_by(
                identity_id=str(identity_id)
            )
            select_res = await s.execute(select_query)
            return select_res.scalar_one_or_none()


async def update_user(message: Message, values: dict) -> Users:
    '''
    Update user in database by `aiogram.types.Message`.


    Args:
        message (`aiogram.types.Message`): Telegram message from user.
        values (dict): Values to update.

    Returns:
        models.Users: User from database.
    '''
    async with get_compyshopdb_session() as s:
        async with s.begin():
            if message.from_user.is_bot:
                identity_id = message.chat.id
            else:
                identity_id = message.from_user.id

            query = sa.update(
                Users
            ).values(
                values
            ).filter_by(
                identity_id=str(identity_id)
            )
            await s.execute(query)

            select_query = sa.select(
                Users
            ).filter_by(
                identity_id=str(identity_id)
            )
            select_res = await s.execute(select_query)
            return select_res.scalar_one_or_none()