from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message

from filters import (
    code_deeplink_filter,
    user_is_salesman_filter,
    user_is_admin_filter,
)
from repositories import SaleRepository
from views import SaleCodeSuccessfullyAppliedView, answer_view

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.text,
    code_deeplink_filter,
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter('*'),
)
async def on_scan_qr_code(
        message: Message,
        client_user_id: int,
        sale_repository: SaleRepository,
) -> None:
    sale = await sale_repository.create_by_user_id(
        client_user_id=client_user_id,
        employee_user_id=message.from_user.id,
    )
    view = SaleCodeSuccessfullyAppliedView(sale)
    await answer_view(message, view)


@router.message(
    F.text,
    code_deeplink_filter,
    StateFilter('*'),
)
async def on_qr_code_scanned_by_non_salesman(message: Message) -> None:
    await message.answer('❌ Вы не являетесь продавцом')
