from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command


from src.tbot import dp
from src.db.queries.user.manage_favorites import (
    add_product_to_favorites, delete_product_from_favorites
)
from src.db.queries.user.manage_user import get_user
from src.db.queries.user.user_states import (
    update_user_state_history, get_current_product_id, clear_user_state_history
)
from src.tbot.user.cards import show_card_first_time


@dp.message(Command('favorites'))
async def show_favorites_list(message: Message):
    await clear_user_state_history(message)
    await update_user_state_history(message, 'start_messaging')
    await update_user_state_history(message, 'show_favorites_list')

    await show_card_first_time(message, favorite=True)


async def add_to_favorites(callback_query: CallbackQuery):
    if isinstance(callback_query, Message):
        message = callback_query
    elif isinstance(callback_query, CallbackQuery):
        message = callback_query.message

    product_id = await get_current_product_id(message)
    user = await get_user(message)

    await add_product_to_favorites(user.user_id, product_id)

    await callback_query.answer(
        text="Товар додано до обраного.",
        show_alert=True
    )


async def delete_from_favorites(callback_query: CallbackQuery):
    if isinstance(callback_query, Message):
        message = callback_query
    elif isinstance(callback_query, CallbackQuery):
        message = callback_query.message

    product_id = await get_current_product_id(message)
    user = await get_user(message)

    await delete_product_from_favorites(user.user_id, product_id)

    await callback_query.answer(
        text="Товар видалено з обраного.",
        show_alert=True
    )