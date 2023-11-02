from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from src.tbot.utils import process_callback_query
from src.tbot.cards import show_catalog_products, show_catalog_list
from src.db.queries.user.user_states import (
    get_current_catalog_id, get_current_product_id,
    update_user_state_history, update_current_product_id
)
from src.db.queries.admin.manage_products import (
    delete_catalog_by_id, delete_product_by_id,
    add_catalog, preapare_add_product, update_product
)


@process_callback_query()
async def add_catalog_title(callback_or_message: CallbackQuery or Message):
    await update_user_state_history(callback_or_message, 'add_catalog_title')

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_btn"
        )
    )

    text="Введіть назву каталогу:"
    await callback_or_message.edit_text(text=text, reply_markup=keyboard.as_markup())


async def finish_catalog_adding(message: Message):
    keyboard = InlineKeyboardBuilder()

    await add_catalog(message.text)

    text="Каталог успішно додано!"
    await message.answer(text=text, reply_markup=keyboard.as_markup())

    await show_catalog_list(message, admin=True)


@process_callback_query()
async def start_adding_product(callback_or_message: CallbackQuery or Message):
    await update_user_state_history(callback_or_message, 'start_adding_product')

    current_catalog_id = await get_current_catalog_id(callback_or_message)
    current_product = await preapare_add_product(current_catalog_id)
    await update_current_product_id(callback_or_message, current_product.product_id)

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_product_creation_btn"
        )
    )

    text="Введіть назву продукту:"
    try:
        await callback_or_message.edit_text(
            text=text,
            reply_markup=keyboard.as_markup()
        )
    except (AttributeError, TelegramBadRequest):
        await callback_or_message.answer(
            text=text,
            reply_markup=keyboard.as_markup()
        )


@process_callback_query()
async def add_product_title_and_process_description(
    callback_or_message: CallbackQuery or Message
):
    await update_user_state_history(
        callback_or_message,
        'add_product_title_and_process_description'
    )

    current_product_id = await get_current_product_id(callback_or_message)
    await update_product(current_product_id, {'title': callback_or_message.text})

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_product_creation_btn"
        )
    )

    text="Введіть опис для продукту:"
    try:
        await callback_or_message.edit_text(
            text=text,
            reply_markup=keyboard.as_markup()
        )
    except (AttributeError, TelegramBadRequest):
        await callback_or_message.answer(
            text=text,
            reply_markup=keyboard.as_markup()
        )


@process_callback_query()
async def add_product_description_and_process_price(
    callback_or_message: CallbackQuery or Message
):
    await update_user_state_history(
        callback_or_message,
        'add_product_description_and_process_price'
    )

    current_product_id = await get_current_product_id(callback_or_message)
    await update_product(current_product_id, {'description': callback_or_message.text})

    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_product_creation_btn"
        )
    )

    text="Введіть ціну для продукту:"
    try:
        await callback_or_message.edit_text(
            text=text,
            reply_markup=keyboard.as_markup()
        )
    except (AttributeError, TelegramBadRequest):
        await callback_or_message.answer(
            text=text,
            reply_markup=keyboard.as_markup()
        )


@process_callback_query()
async def add_product_price_and_finish_adding(
    callback_or_message: CallbackQuery or Message
):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_product_creation_btn"
        )
    )

    current_product_id = await get_current_product_id(callback_or_message)
    try:
        price = float(callback_or_message.text)
    except ValueError:
        text="Значення повинно бути числом!"

        await callback_or_message.answer(
            text=text,
            reply_markup=keyboard.as_markup()
        )
        return

    await update_product(current_product_id, {'price': price})

    text="Продукт додано!"

    await callback_or_message.answer(
        text=text
    )

    await update_user_state_history(
        callback_or_message,
        'show_catalog_list',
        clear=True
    )
    await show_catalog_products(callback_or_message, admin=True)


async def delete_catalog(callback_query: CallbackQuery):
    current_catalog = await get_current_catalog_id(callback_query.message)
    await delete_catalog_by_id(current_catalog)

    await callback_query.answer('Каталог успішно видалено!', show_alert=True)
    await callback_query.message.delete()

    await show_catalog_list(callback_query, admin=True)


async def delete_product(callback_query: CallbackQuery):
    current_product = await get_current_product_id(callback_query.message)
    await delete_product_by_id(current_product)

    await callback_query.answer('Товар успішно видалено!', show_alert=True)
    await callback_query.message.delete()

    await show_catalog_products(callback_query, admin=True)
