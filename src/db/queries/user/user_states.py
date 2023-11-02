import sqlalchemy as sa
from aiogram.types import Message

from src.db.models import UserStates
from src.db.session import get_compyshopdb_session
from src.db.queries.user.manage_user import get_user


async def update_user_state_history(
    message: Message,
    state: str,
    clear:bool=None
) -> None:
    """
    Update user state history in database by `aiogram.types.Message`.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.
        state (str): State to add to the user's state history.
        clear (bool): Whether to clear the user's state history before adding
            the new state.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        select_query = sa.select(UserStates).filter_by(user_id=user.user_id)
        select_result = await s.execute(select_query)
        user_state = select_result.scalar_one_or_none()

        if clear and user_state is not None:
            user_state.history.clear()
            await s.commit()

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(select_query)
        user_state = select_result.scalar_one_or_none()

        if user_state is None:
            user_state = UserStates(
                user_id=user.user_id,
                history=[state]
            )
            s.add(user_state)
        else:
            if len(user_state.history) == 0:
                update_query = sa.update(
                    UserStates
                ).values(
                    history=[state]
                ).filter_by(
                    user_id=user.user_id
                )
                await s.execute(update_query)
            else:
                if user_state.history[-1] != state:
                    user_state.history.append(state)

        await s.commit()


async def update_and_get_previous_user_state(message: Message) -> str:
    """
    Update user state history in database by `aiogram.types.Message`.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        str: The previous state of the user.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        user_state.history.pop(-1)
        element = user_state.history[-1]

        await s.commit()

        return element


async def get_current_user_state(message: Message) -> str:
    """
    Get the current state of the user.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        str: The current state of the user.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        return user_state.history[-1]


async def update_current_product_id(message: Message, product_id: int) -> int:
    """
    Update the current product ID of the user.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.
        product_id (int): The ID of the product to set as the current product.

    Returns:
        int: The ID of the current product.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        async with s.begin():
            update_query = sa.update(
                UserStates
            ).values(
                current_product_id=product_id
            ).filter_by(
                user_id=user.user_id
            )
            await s.execute(update_query)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        return user_state.current_product_id


async def get_current_product_id(message: Message) -> int:
    """
    Get the current product ID of the user.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        int: The ID of the current product.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        return user_state.current_product_id


async def update_current_catalog_id(message: Message, catalog_id: int) -> int:
    """
    Update the current catalog ID of the user.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.
        catalog_id (int): The ID of the catalog to set as the current catalog.

    Returns:
        int: The ID of the current catalog.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        async with s.begin():
            update_query = sa.update(
                UserStates
            ).values(
                current_catalog_id=catalog_id
            ).filter_by(
                user_id=user.user_id
            )
            await s.execute(update_query)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        return user_state.current_catalog_id


async def get_current_catalog_id(message: Message) -> int:
    """
    Get the current catalog ID of the user.

    Args:
        message (`aiogram.types.Message`): Telegram message from user.

    Returns:
        int: The ID of the current catalog.
    """
    user = await get_user(message)

    async with get_compyshopdb_session() as s:
        select_result = await s.execute(
            sa.select(UserStates).filter_by(user_id=user.user_id)
        )
        user_state = select_result.scalar_one_or_none()

        return user_state.current_catalog_id