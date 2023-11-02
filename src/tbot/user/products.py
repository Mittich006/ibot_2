from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.tbot import dp
from src.db.queries.user.user_states import (
    update_user_state_history, get_current_product_id
)
from src.tbot.utils import process_callback_query



@process_callback_query()
async def buy_product(callback_query: CallbackQuery):
    await update_user_state_history(callback_query, 'buy_product')

    current_product_id = await get_current_product_id(callback_query)

    keyboard = InlineKeyboardBuilder()

    btn_texts = ["1", "2", "3", "5", "10", "20"]

    for text in btn_texts:
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=f"buy_{text}_{current_product_id}"
            )
        )

    keyboard.adjust(3)

    await callback_query.edit_text(
        text="Оберіть кількість товару:",
        reply_markup=keyboard.as_markup()
    )


async def try_to_confirm_buying_product(callback_query: CallbackQuery):
    if isinstance(callback_query, Message):
        message = callback_query
    elif isinstance(callback_query, CallbackQuery):
        message = callback_query.message

    current_product_id = await get_current_product_id(message)

    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text="Підтвердити",
            callback_data=f"confirm_buy_{current_product_id}"
        ),
        InlineKeyboardButton(
            text="Скасувати",
            callback_data=f"cancel_buy_{current_product_id}"
        )
    )

    quantity = callback_query.data.split("_")[1]

    await message.edit_text(
        text=f"Ви впевнені, що хочете придбати даний "
             f"товар в кількості {quantity}?",
        reply_markup=keyboard.as_markup()
    )


async def confirm_buying_product(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Ви успішно придбали товар!",
        show_alert=True
    )


async def cancel_buying_product(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Ви скасували покупку товару!",
        show_alert=True
    )