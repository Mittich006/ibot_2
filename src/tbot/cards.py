from traceback import print_exc

from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

from src.tbot import dp
from src.db.queries.user.manage_products import (
    get_all_products_by_catalog, get_all_products_by_ids
)
from src.tbot.utils import (
    construct_product_card_keyboard, process_callback_query,
    add_arrows_to_card_keyboard, construct_and_send_product_card,
    construct_catalog_list_keyboard
)
from src.db.queries.user.user_states import (
    update_user_state_history, update_current_catalog_id,
    get_current_product_id, get_current_catalog_id,
    update_current_product_id
)
from src.db.queries.user.manage_products import (
    get_all_catalogs, get_catalog_id_by_title, get_catalog_title_by_id
)
from src.db.queries.user.manage_favorites import get_all_favorites_ids
from src.db.queries.user.manage_user import get_user


@dp.message(Command('products'))
async def show_catalog_list(
    callback_or_message: CallbackQuery or Message,
    admin: bool = False
) -> None:
    """
    This handler receives messages with `/catalog` command.
    """

    if isinstance(callback_or_message, Message):
        message = callback_or_message
    elif isinstance(callback_or_message, CallbackQuery):
        message = callback_or_message.message

    await update_user_state_history(message, 'show_catalog_list')

    catalogs = await get_all_catalogs()
    if not len(catalogs) == 0:
        keyboard_btns = {catalog.title: catalog.title for catalog in catalogs}
        keyboard = await construct_catalog_list_keyboard(keyboard_btns, admin=admin)

        text="Оберіть каталог:"
        reply_markup=keyboard.as_markup()
    else:
        keyboard = InlineKeyboardBuilder()

        if admin:
            keyboard.row(
                InlineKeyboardButton(
                    text="Додати каталог",
                    callback_data="admin_add_catalog"
                )
            )

        keyboard.row(
            InlineKeyboardButton(
                text="Назад",
                callback_data="back_btn"
            )
        )

        text="На даний момент каталоги відсутні."
        reply_markup=keyboard.as_markup()

    if admin:
        try:
            await message.edit_text(text=text, reply_markup=reply_markup)
        except TelegramBadRequest:
            await message.answer(text=text, reply_markup=reply_markup)
    else:
        await message.answer(text=text, reply_markup=reply_markup)



async def show_catalog_products(
    callback_query: CallbackQuery,
    admin: bool = False
) -> None:
    """
    This handler receives callback queries from inline keyboards.
    """

    if isinstance(callback_query, Message):
        message = callback_query
        catalog_id = await get_current_catalog_id(message)
        catalog_title = await get_catalog_title_by_id(catalog_id)
    elif isinstance(callback_query, CallbackQuery):
        message = callback_query.message
        catalog_title = callback_query.data
        catalog_id = await get_catalog_id_by_title(catalog_title)


    await update_user_state_history(message, 'show_catalog_products')

    if catalog_id is not None:
        await update_current_catalog_id(message, catalog_id)

    await show_card_first_time(message, admin=admin)

    if isinstance(callback_query, CallbackQuery):
        await callback_query.answer()


@process_callback_query()
async def show_card_first_time(
    callback_query: CallbackQuery,
    favorite: bool = False,
    admin: bool = False
) -> None:
    if favorite:
        if isinstance(callback_query, Message):
            user = await get_user(callback_query)
        else:
            user = await get_user(callback_query.message)

        keyboard = await construct_product_card_keyboard(favorite=True)
        user_favorites = await get_all_favorites_ids(user.user_id)
        products = await get_all_products_by_ids(user_favorites)
    else:
        keyboard = await construct_product_card_keyboard(admin=admin)
        current_catalog_id = await get_current_catalog_id(callback_query)
        products = await get_all_products_by_catalog(current_catalog_id)

    if len(products) == 0:
        keyboard = InlineKeyboardBuilder()

        if admin:
            keyboard.row(*[
                InlineKeyboardButton(
                    text="Додати товар до каталогу",
                    callback_data="admin_add_product"
                ),
                InlineKeyboardButton(
                    text="Видалити каталог",
                    callback_data="admin_delete_catalog"
                )
        ])

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


async def change_product_card(
    callback_query: CallbackQuery,
    favorite: bool = False,
    admin: bool = False
):
    try:
        if favorite:
            if isinstance(callback_query, Message):
                user = await get_user(callback_query)
            else:
                user = await get_user(callback_query.message)

            keyboard = await construct_product_card_keyboard(favorite=True)
            user_favorites = await get_all_favorites_ids(user.user_id)
            products = await get_all_products_by_ids(user_favorites)
        else:
            keyboard = await construct_product_card_keyboard(admin=admin)
            current_catalog_id = await get_current_catalog_id(callback_query)
            products = await get_all_products_by_catalog(current_catalog_id)
            

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
    except Exception:
        print_exc()