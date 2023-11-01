from aiogram import F
from aiogram.types import Message, CallbackQuery

from src.tbot import dp
from src.db.queries.user.user_states import (
    get_current_user_state, update_and_get_previous_user_state
)
from src.tbot.start_messaging import register_user_and_construct_menu
from src.tbot.user.products import (
    buy_product, try_to_confirm_buying_product, confirm_buying_product,
    cancel_buying_product, get_current_product_id
)
from src.tbot.user.search import search_product
from src.tbot.user.cards import change_product_card

from src.tbot.global_handler import *
from src.tbot.start_messaging import *
from src.tbot.user.favorites import *
from src.tbot.user.products import *
from src.tbot.user.search import *


@dp.callback_query(F.data == 'back_btn')
async def back_btn(callback_query: CallbackQuery):
    try:
        message = callback_query.message
    except AttributeError:
        message = callback_query

    previous_state = await update_and_get_previous_user_state(message)

    await message.delete()

    await eval(previous_state)(message)


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

    elif current_state == 'show_catalog_products' and (
        callback_query.data == 'next_product'\
            or callback_query.data == 'prev_product'
        ):
        await change_product_card(callback_query)

    elif current_state == 'show_catalog_products' and\
        callback_query.data == 'buy_product':
        await buy_product(callback_query)

    elif current_state == 'show_catalog_products' and\
        callback_query.data == 'search_product':
        await search_product(callback_query)

    elif current_state == 'show_catalog_products' and\
        callback_query.data == 'add_to_favorites':
        await add_to_favorites(callback_query)

    elif current_state == 'buy_product':
        current_product_id = await get_current_product_id(callback_query.message)

        if callback_query.data == f'confirm_buy_{current_product_id}':
            await confirm_buying_product(callback_query)
            await back_btn(callback_query)
        elif callback_query.data == f'cancel_buy_{current_product_id}':
            await cancel_buying_product(callback_query)
            await back_btn(callback_query)
        else:
            await try_to_confirm_buying_product(callback_query)

    elif current_state == 'show_favorites_list' and (
        callback_query.data == 'next_product'\
            or callback_query.data == 'prev_product'
        ):
        await change_product_card(callback_query, favorite=True)

    elif current_state == 'show_favorites_list' and\
        callback_query.data == 'buy_product':
        await buy_product(callback_query)

    elif current_state == 'show_favorites_list' and\
        callback_query.data == 'search_product':
        await search_product(callback_query)

    elif current_state == 'show_favorites_list' and\
        callback_query.data == 'delete_from_favorites':
        await delete_from_favorites(callback_query)
        await show_card_first_time(callback_query, favorite=True)
