from aiogram.types import CallbackQuery


async def get_admin_statistics(callback_query: CallbackQuery):
    await callback_query.answer(
        text="Ще не реалізовано.",
        show_alert=True
    )