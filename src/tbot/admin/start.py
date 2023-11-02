from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.queries.user.manage_user import update_user
from src.tbot.utils import process_callback_query


@process_callback_query()
async def register_admin_and_construct_start_messaging(
        callback_or_message: CallbackQuery or Message
    ):
    user = await update_user(
        callback_or_message, {
            'registered': True,
            'admin': True
            }
        )

    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text="Управління продуктами та каталогами",
            callback_data='admin_manage_products'
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text="Отримати статистику",
            callback_data='admin_get_statistics'
        )
    )

    await callback_or_message.answer(
        text=f"Вітаю, адміне, {user.first_name}!\n\nОберіть дію:",
        reply_markup=keyboard.as_markup()
    )
