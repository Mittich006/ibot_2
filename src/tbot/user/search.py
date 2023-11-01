from aiogram.types import CallbackQuery


async def search_product(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Ще не реалізовано.",
        show_alert=True
    )