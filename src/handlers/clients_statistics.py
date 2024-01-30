from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message

from filters import user_is_admin_filter
from repositories import SaleRepository
from views import ClientsStatisticsView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text == '📊 Статистика по клиентам',
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_show_clients_statistics(
        message: Message,
        sale_repository: SaleRepository,
        bot: Bot,
) -> None:
    clients_statistics = await sale_repository.get_statistics(bot_id=bot.id)
    view = ClientsStatisticsView(clients_statistics)
    await answer_view(message, view)
