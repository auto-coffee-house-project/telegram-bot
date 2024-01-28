from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from callback_data import SalesmanDeleteCallbackData
from filters import user_is_admin_filter
from repositories import SalesmanRepository
from views import SalesmanListView, edit_view

__all__ = ('router',)

router = Router(name=__name__)


@router.callback_query(
    SalesmanDeleteCallbackData.filter(),
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_salesman_delete_callback_data(
        callback_query: CallbackQuery,
        callback_data: SalesmanDeleteCallbackData,
        salesman_repository: SalesmanRepository,
) -> None:
    await salesman_repository.delete_by_user_id(callback_data.user_id)
    await callback_query.answer('Продавец удален', show_alert=True)
    shop_salesmans = await salesman_repository.get_all(
        admin_user_id=callback_query.from_user.id,
    )
    view = SalesmanListView(shop_salesmans)
    await edit_view(callback_query.message, view)
