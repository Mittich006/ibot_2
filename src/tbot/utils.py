from aiogram.types import (
    Message, BotCommand, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def construct_commands(message: Message):
    commands = [
        BotCommand(
            command='/products',
            description='Переглянути доступні товари магазину.'
        ),
        BotCommand(
            command='/favorites',
            description='Переглянути збережені до улюблених товари.'
        )
    ]
    await message.bot.set_my_commands(commands)


async def construct_product_card_keyboard() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    buy_and_fav_elements = [
        InlineKeyboardButton(
            text="Додати до улюблених",
            callback_data="add_to_favorites"
        ),
        InlineKeyboardButton(
            text="Придбати",
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
            callback_data="back_to_catalog_list"
        )
    ]

    keyboard.row(*buy_and_fav_elements)
    keyboard.row(*search_and_back_elements)

    return keyboard