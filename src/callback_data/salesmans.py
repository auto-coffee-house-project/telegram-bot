from aiogram.filters.callback_data import CallbackData

__all__ = ('SalesmanDeleteCallbackData',)


class SalesmanDeleteCallbackData(CallbackData, prefix='salesman-delete'):
    user_id: int
