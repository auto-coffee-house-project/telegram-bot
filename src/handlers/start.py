from aiogram import Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters import (
    user_is_salesman_filter,
    user_is_admin_filter,
    user_is_client_filter,
)
from repositories import BotRepository
from views import (
    StartClientView,
    answer_photo_view,
    StartSalesmanView,
    answer_view,
    StartAdminView,
)

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    CommandStart(),
    user_is_salesman_filter,
    StateFilter('*'),
)
async def on_start_salesman(
        message: Message,
        state: FSMContext,
) -> None:
    view = StartSalesmanView()
    await answer_view(message, view)
    await state.clear()


@router.message(
    CommandStart(),
    user_is_admin_filter,
    StateFilter('*'),
)
async def on_start_admin(
        message: Message,
        state: FSMContext,
) -> None:
    view = StartAdminView()
    await answer_view(message, view)
    await state.clear()


@router.message(
    CommandStart(),
    user_is_client_filter,
    StateFilter('*'),
)
async def on_start_client(
        message: Message,
        state: FSMContext,
        bot: Bot,
        bot_repository: BotRepository,
) -> None:
    bot = await bot_repository.get_by_id(bot.id)
    view = StartClientView(start_text=bot.start_text)
    await answer_photo_view(message, view)
    await state.clear()
