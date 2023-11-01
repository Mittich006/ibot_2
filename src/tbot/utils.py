from typing import Union
from functools import wraps

from aiogram.types import (
    Message, BotCommand, InlineKeyboardButton, CallbackQuery
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

from src.db.queries.user.user_states import update_user_state_history
from src.db.models import Products


async def construct_commands(message: Message):
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


async def construct_catalog_list_keyboard(btns: dict) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for btn_text, btn_data in btns.items():
        keyboard.add(
            InlineKeyboardButton(
                text=btn_text,
                callback_data=btn_data
            )
        )

    keyboard.adjust(int(len(btns)/2))

    keyboard.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_btn"
        )
    )

    return keyboard


async def construct_product_card_keyboard(
    favorite: bool = None
) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    if favorite:
        buy_and_fav_elements = [
            InlineKeyboardButton(
                text="Видалити з обраного",
                callback_data="delete_from_favorites"
            ),
            InlineKeyboardButton(
                text="Придбати товар",
                callback_data="buy_product"
            )
        ]
    else:
        buy_and_fav_elements = [
            InlineKeyboardButton(
                text="Додати до обраного",
                callback_data="add_to_favorites"
            ),
            InlineKeyboardButton(
                text="Придбати товар",
                callback_data="buy_product"
            )
        ]

    search_and_back_elements = [
        InlineKeyboardButton(
            text="Пошук",
            callback_data="search_product"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="back_btn"
        )
    ]

    keyboard.row(*buy_and_fav_elements)
    keyboard.row(*search_and_back_elements)

    return keyboard


async def add_arrows_to_card_keyboard(
    keyboard: InlineKeyboardBuilder
) -> InlineKeyboardBuilder:
    keyboard.row(
        InlineKeyboardButton(
            text="<--",
            callback_data="prev_product"
        ),
        InlineKeyboardButton(
            text="-->",
            callback_data="next_product"
        )
    )

    return keyboard


async def construct_and_send_product_card(
    callback_or_message: CallbackQuery or Message,
    product: Products,
    keyboard: InlineKeyboardBuilder
) -> None:
    text = f'Назва: {product.title}\n' \
              f'Ціна: {product.price}\n\n' \
              f'Опис: {product.description}\n'

    if isinstance(callback_or_message, CallbackQuery):
        message = callback_or_message.message
    elif isinstance(callback_or_message, Message):
        message = callback_or_message

    try:
        await message.edit_text(
            text=text,
            reply_markup=keyboard.as_markup()
        )
    except TelegramBadRequest:
        await message.answer(
            text=text,
            reply_markup=keyboard.as_markup()
        )


def process_callback_query():
    def wrapper(func):
        wraps(func)
        async def wrapped(callback_query: Union[Message, CallbackQuery], *args, **kwargs):
            if isinstance(callback_query, Message):
                message = callback_query
            elif isinstance(callback_query, CallbackQuery):
                message = callback_query.message

            await func(message, *args, **kwargs)

            if isinstance(callback_query, CallbackQuery):
                await callback_query.answer()

        return wrapped
    return wrapper
