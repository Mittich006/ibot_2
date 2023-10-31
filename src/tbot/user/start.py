from aiogram import F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from sqlalchemy.exc import IntegrityError

from src.tbot import dp
from src.db.session import get_compyshopdb_session, select, insert
from src.db.models import Users
from src.logger import logger


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(F.text == "db_test")
async def db_test(message: Message) -> None:
    try:
        async with get_compyshopdb_session() as session:
            async with session.begin():
                query = insert(
                    Users
                ).values(
                    identity_id=str(message.from_user.id),
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                )

                await session.execute(query)
    except IntegrityError:
        pass

    try:
        async with get_compyshopdb_session() as session:
            query = select(
                Users
            ).where(
                Users.identity_id == str(message.from_user.id)
            )

            result = await session.scalars(query)
            data = result.one_or_none()

        await message.answer(data.username)
    except Exception as e:
        logger.error(e)