from aiogram import Router, F
from aiogram.filters import StateFilter, or_f
from aiogram.types import Message

from filters import (
    code_deeplink_filter,
    user_is_salesman_filter,
    user_is_admin_filter,
)
from repositories import SaleRepository
from views import SaleTemporaryCodeSuccessfullyAppliedView, answer_view

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
        code: str,
        sale_repository: SaleRepository,
) -> None:
    sale = await sale_repository.create(
        code=code,
        salesman_user_id=message.from_user.id,
    )
    view = SaleTemporaryCodeSuccessfullyAppliedView(sale)
    await answer_view(message, view)


@router.message(
    F.text,
    code_deeplink_filter,
    StateFilter('*'),
)
async def on_qr_code_scanned_by_non_salesman(message: Message) -> None:
    await message.answer('❌ Вы не являетесь продавцом')
