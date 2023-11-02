from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart, Command

from src.tbot import dp, bot
from src.tbot.user.start import register_user_and_construct_menu
from src.tbot.admin.start import register_admin_and_construct_start_messaging
from src.db.queries.user.manage_user import get_or_create_user
from src.db.queries.user.user_states import update_user_state_history


@dp.message(CommandStart())
async def start_user_messaging(message: Message) -> None:
    """
    This handler receives messages with `/start` command.
    """

    user = await get_or_create_user(message)
    await update_user_state_history(message, 'start_user_messaging', clear=True)

    if user.registered:
        await register_user_and_construct_menu(message)
        return

    keyboard_btns = [
        [
            InlineKeyboardButton(text=user.first_name, callback_data='username')
        ],
    ]
    keyboard = InlineKeyboardBuilder(keyboard_btns)

    await bot.set_my_commands([])

    await message.answer(
        text="Як до Вас звертатися?",
        reply_markup=keyboard.as_markup()
    )


@dp.message(Command('startadmin'))
async def start_admin_messaging(message: Message) -> None:
    """
    This handler receives messages with `/startadmin` command.
    """

    user = await get_or_create_user(message)
    await update_user_state_history(message, 'start_admin_messaging', clear=True)

    await register_admin_and_construct_start_messaging(message)
