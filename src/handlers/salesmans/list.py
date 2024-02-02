from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import user_is_admin_filter
from repositories import SalesmanRepository
from views import SalesmanListView, answer_view

__all__ = ('router',)
router = Router(name=__name__)


@router.message(
    F.text == '👥 Продавцы',
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_salesmans_list(
        message: Message,
        salesman_repository: SalesmanRepository,
        bot: Bot,
) -> None:
    admin_user_id = message.from_user.id
    shop_salesmans = await salesman_repository.get_all(
        admin_user_id=admin_user_id,
        bot_id=bot.id,
    )
    view = SalesmanListView(shop_salesmans)
    await answer_view(message, view)
