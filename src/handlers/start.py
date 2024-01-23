from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

from filters import salesman_filter
from models import Salesman
from repositories import ShopGroupRepository
from views import (
    StartClientView, answer_photo_view, StartSalesmanView,
    answer_view
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    CommandStart(),
    salesman_filter,
    StateFilter('*'),
)
async def on_start_salesman(
        message: Message,
) -> None:
    view = StartSalesmanView()
    await answer_view(message, view)


@router.message(CommandStart(), StateFilter('*'))
async def on_start_client(
        message: Message,
        bot: Bot,
        shop_group_repository: ShopGroupRepository,
) -> None:
    shop_group = await shop_group_repository.get_by_bot_id(bot.id)
    view = StartClientView(shop_group.each_nth_cup_free)
    await answer_photo_view(message, view)
