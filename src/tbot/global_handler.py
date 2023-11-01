from aiogram import F
from aiogram.types import Message, CallbackQuery

from src.tbot import dp
from src.db.queries.user.user_states import get_current_user_state
from src.tbot.start_messaging import register_user_and_construct_menu
from src.tbot.user.products import (
    show_catalog_products, next_product, prev_product
)


@dp.message(F.text)
async def global_message_handler(message: Message) -> None:
    current_state = await get_current_user_state(message)

    if current_state == 'start_messaging':
        await register_user_and_construct_menu(message, message.text)

@dp.callback_query(lambda callback_query: True)
async def global_callback_handler(callback_query: CallbackQuery) -> None:
    current_state = await get_current_user_state(callback_query.message)

    if current_state == 'show_catalog_list':
        await show_catalog_products(callback_query)

    elif current_state == 'viewing_product_card' and callback_query.data == 'next_product':
        await next_product(callback_query)
    
    elif current_state == 'viewing_product_card' and callback_query.data == 'prev_product':
        await prev_product(callback_query)
