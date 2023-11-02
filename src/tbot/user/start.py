from aiogram import F
from aiogram.types import Message, CallbackQuery, BotCommand

from src.tbot import dp
from src.db.queries.user.manage_user import update_user


async def construct_commands_for_user(message: Message):
    commands = [
        BotCommand(
            command='/products',
            description='Каталог товарів.'
        ),
        BotCommand(
            command='/favorites',
            description='Обране.'
        )
    ]
    await message.bot.set_my_commands(commands)


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

    if first_time:
        await message.delete()

    if custom_first_name:
        await update_user(message, {'first_name': custom_first_name})

    user = await update_user(message, {
        'registered': True,
        'admin': False
        }
    )

    await construct_commands_for_user(message)

    await message.answer(
        text=f"Вітаю, {user.first_name}!\n"
        f"Ви успішно зареєстровані! Для роботи з ботом використовуйте команди в меню.\n"
        f"Якщо меню не відображається, перезайдіть в чат з ботом.",
    )

    if isinstance(callback_or_message, CallbackQuery):
        await callback_or_message.answer()