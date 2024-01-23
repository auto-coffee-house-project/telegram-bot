from aiogram.filters.callback_data import CallbackData

__all__ = ('SaleDeleteCallbackData',)


class SaleDeleteCallbackData(CallbackData, prefix='sale-delete'):
    sale_id: int
