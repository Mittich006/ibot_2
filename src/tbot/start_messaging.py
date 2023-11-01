from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart

from src.tbot import dp, bot
from src.tbot.utils import construct_commands
from src.db.queries.user.manage_user import (
    get_or_create_user, update_user
)
from src.db.queries.user.user_states import (
    update_user_state_history, clear_user_state_history
)


@dp.message(CommandStart())
async def start_messaging(message: Message) -> None:
    """
    This handler receives messages with `/start` command.
    """

    user = await get_or_create_user(message)
    await update_user_state_history(message, 'start_messaging')

    if user.registered:
        await clear_user_state_history(message)
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


@dp.callback_query(F.data == 'username')
async def register_user_and_construct_menu(
    callback_or_message: CallbackQuery or Message,
    custom_first_name: str = None,
    first_time: bool = False
):
    if isinstance(callback_or_message, Message):
        message = callback_or_message
    elif isinstance(callback_or_message, CallbackQuery):
        message = callback_or_message.message

    await update_user_state_history(message, 'register_user_and_construct_menu')

    if first_time:
        await message.delete()

    if custom_first_name:
        await update_user(message, {'first_name': custom_first_name})

    user = await update_user(message, {'registered': True})

    await construct_commands(message)

    await message.answer(
        text=f"Вітаю, {user.first_name}!\n"
        f"Ви успішно зареєстровані! Для роботи з ботом використовуйте команди в меню.\n"
        f"Якщо меню не відображається, перезайдіть в чат з ботом.",
    )

    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.answer()