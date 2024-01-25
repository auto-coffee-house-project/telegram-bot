from aiogram import Router
from aiogram.filters import StateFilter, ExceptionTypeFilter
from aiogram.types import CallbackQuery, ErrorEvent

from callback_data import SaleDeleteCallbackData
from exceptions import SaleDeletionTimeExpiredError
from filters import user_is_salesman_filter
from repositories import SaleRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.error(ExceptionTypeFilter(SaleDeletionTimeExpiredError))
async def on_sale_deletion_time_expired_error(event: ErrorEvent) -> None:
    if event.update.callback_query is not None:
        callback_query = event.update.callback_query
        await callback_query.answer(
            text='❌ Время отмены продажи истекло',
            show_alert=True,
        )
        await callback_query.message.edit_text(
            f'{callback_query.message.text}\n\n<i>[Время отмены истекло]</i>'
        )


@router.callback_query(
    SaleDeleteCallbackData.filter(),
    user_is_salesman_filter,
    StateFilter('*'),
)
async def on_cancel_sale(
        callback_query: CallbackQuery,
        sale_repository: SaleRepository,
        callback_data: SaleDeleteCallbackData,
) -> None:
    await sale_repository.delete(callback_data.sale_id)
    await callback_query.answer(
        text='✅ Продажа отменена',
        show_alert=True,
    )
    await callback_query.message.edit_text(
        f'{callback_query.message.text}\n\n<i>[Отменено]</i>'
    )
