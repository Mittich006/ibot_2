from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.db.queries.user.user_states import (
    update_current_product_id, get_current_product_id,
    get_current_catalog_id
)
from src.db.queries.user.manage_products import (
    get_all_products_by_catalog, get_all_products_by_ids
)
from src.tbot.utils import (
    construct_product_card_keyboard, process_callback_query,
    add_arrows_to_card_keyboard, construct_and_send_product_card
)
from src.db.queries.user.manage_favorites import get_all_favorites_ids
from src.db.queries.user.manage_user import get_user


@process_callback_query()
async def show_card_first_time(
    callback_query: CallbackQuery,
    favorite: bool = False
) -> None:
    if favorite:
        if isinstance(callback_query, Message):
            user = await get_user(callback_query)
        else:
            user = await get_user(callback_query.message)

        user_favorites = await get_all_favorites_ids(user.user_id)
        products = await get_all_products_by_ids(user_favorites)
        keyboard = await construct_product_card_keyboard(favorite=True)
    else:
        catalog_id = await get_current_catalog_id(callback_query)
        products = await get_all_products_by_catalog(catalog_id)
        keyboard = await construct_product_card_keyboard()

    if len(products) == 0:
        keyboard = InlineKeyboardBuilder()

        keyboard.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_btn"
            )
        )

        await callback_query.answer(
            text="На даний момент товари відсутні.",
            reply_markup=keyboard.as_markup()
        )
        return

    await update_current_product_id(callback_query, products[0].product_id)

    if len(products) > 1:
        keyboard.row(
            InlineKeyboardButton(
                text="-->",
                callback_data="next_product"
            )
        )

    await construct_and_send_product_card(
        callback_query, products[0], keyboard
    )


async def change_product_card(callback_query: CallbackQuery, favorite: bool = False):
    if favorite:
        if isinstance(callback_query, Message):
            user = await get_user(callback_query)
        else:
            user = await get_user(callback_query.message)

        user_favorites = await get_all_favorites_ids(user.user_id)
        products = await get_all_products_by_ids(user_favorites)
        keyboard = await construct_product_card_keyboard(favorite=True)
    else:
        current_catalog_id = await get_current_catalog_id(callback_query)
        products = await get_all_products_by_catalog(current_catalog_id)
        keyboard = await construct_product_card_keyboard()

    if len(products) > 1:
        current_product_id = await get_current_product_id(callback_query)

        for i, product in enumerate(products):
            if product.product_id == current_product_id:
                if callback_query.data == 'prev_product':
                    if i == 1:
                        keyboard.row(
                            InlineKeyboardButton(
                                text="-->",
                                callback_data="next_product"
                            )
                        )
                    else:
                        keyboard = await add_arrows_to_card_keyboard(keyboard)

                    current_product = products[i - 1]
                    await update_current_product_id(
                        callback_query, current_product.product_id
                    )
                elif callback_query.data == 'next_product':
                    if i == len(products) - 2:
                        keyboard.row(
                            InlineKeyboardButton(
                                text="<--",
                                callback_data="prev_product"
                            )
                        )
                    else:
                        keyboard = await add_arrows_to_card_keyboard(keyboard)

                    current_product = products[i + 1]
                    await update_current_product_id(
                        callback_query, current_product.product_id
                    )
    else:
        current_product = products[0]
        await update_current_product_id(
            callback_query, current_product.product_id
        )

    await construct_and_send_product_card(
        callback_query, current_product, keyboard
    )