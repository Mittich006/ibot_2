import traceback

from aiogram import F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from src.tbot import dp
from src.db.queries.user.user_states import (
    update_user_state_history, update_current_catalog_id,
    update_current_product_id, get_current_product_id,
    get_current_catalog_id
)
from src.db.queries.user.manage_products import (
    get_all_catalogs, get_catalog_id_by_title, get_all_products_by_catalog,
    get_product_by_id
)
from src.tbot.utils import construct_product_card_keyboard


@dp.message(Command('products'))
async def show_catalog_list(message: Message) -> None:
    """
    This handler receives messages with `/catalog` command.
    """
    await update_user_state_history(message, 'show_catalog_list')

    catalogs = await get_all_catalogs()

    keyboard_btns = []
    for catalog in catalogs:
        keyboard_btns.append([
            InlineKeyboardButton(
                text=catalog.title,
                callback_data=catalog.title
            )
        ])

    keyboard = InlineKeyboardBuilder(keyboard_btns)

    await message.answer(
        text="Оберіть каталог:",
        reply_markup=keyboard.as_markup()
    )


async def show_catalog_products(callback_query: CallbackQuery) -> None:
    """
    This handler receives callback queries from inline keyboards.
    """

    await update_user_state_history(callback_query.message, 'show_catalog_products')

    catalog_title = callback_query.data
    catalog_id = await get_catalog_id_by_title(catalog_title)

    await update_current_catalog_id(callback_query.message, catalog_id)

    await callback_query.message.answer(
        text=f"Ви обрали каталог: {catalog_title}"
    )

    await callback_query.answer()

    await show_product_card_first_time(callback_query)


async def show_product_card_first_time(callback_query: CallbackQuery) -> None:
    await update_user_state_history(callback_query.message, 'viewing_product_card')

    catalog_id = await get_current_catalog_id(callback_query.message)
    products = await get_all_products_by_catalog(catalog_id)
    await update_current_product_id(callback_query.message, products[0].product_id)

    keyboard = await construct_product_card_keyboard()

    keyboard.row(
        InlineKeyboardButton(
            text="-->",
            callback_data="next_product"
        )
    )

    text = f'Назва: {products[0].title}\n' \
              f'Ціна: {products[0].price}\n' \
              f'Опис: {products[0].description}\n'

    await callback_query.message.answer(
        text=text,
        reply_markup=keyboard.as_markup()
    )


async def next_product(callback_query: CallbackQuery):
    current_product_id = await get_current_product_id(callback_query.message)
    current_catalog_id = await get_current_catalog_id(callback_query.message)

    products = await get_all_products_by_catalog(current_catalog_id)
    keyboard = await construct_product_card_keyboard()

    for i, product in enumerate(products):
        if product.product_id == current_product_id:
            if i == len(products) - 2:
                keyboard.row(
                    InlineKeyboardButton(
                        text="<--",
                        callback_data="prev_product"
                    )
                )
            else:
                keyboard.row(*[
                    InlineKeyboardButton(
                        text="<--",
                        callback_data="prev_product"
                    ),
                    InlineKeyboardButton(
                        text="-->",
                        callback_data="next_product"
                    )
                ])


            await update_current_product_id(callback_query.message, products[i + 1].product_id)

            text = f'Назва: {products[i + 1].title}\n' \
                   f'Ціна: {products[i + 1].price}\n' \
                   f'Опис: {products[i + 1].description}\n'

            await callback_query.message.edit_text(
                text=text,
                reply_markup=keyboard.as_markup()
            )

            await callback_query.answer()
            return

async def prev_product(callback_query: CallbackQuery):
    current_product_id = await get_current_product_id(callback_query.message)
    current_catalog_id = await get_current_catalog_id(callback_query.message)

    products = await get_all_products_by_catalog(current_catalog_id)
    keyboard = await construct_product_card_keyboard()

    for i, product in enumerate(products):
        if product.product_id == current_product_id:
            if i == 1:
                keyboard.row(
                    InlineKeyboardButton(
                        text="-->",
                        callback_data="next_product"
                    )
                )
            else:
                keyboard.row(*[
                    InlineKeyboardButton(
                        text="<--",
                        callback_data="prev_product"
                    ),
                    InlineKeyboardButton(
                        text="-->",
                        callback_data="next_product"
                    )
                ])

            await update_current_product_id(callback_query.message, products[i - 1].product_id)

            text = f'Назва: {products[i - 1].title}\n' \
                   f'Ціна: {products[i - 1].price}\n' \
                   f'Опис: {products[i - 1].description}\n'

            await callback_query.message.edit_text(
                text=text,
                reply_markup=keyboard.as_markup()
            )

            await callback_query.answer()
            return
