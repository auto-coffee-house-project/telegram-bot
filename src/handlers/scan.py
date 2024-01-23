from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from callback_data import code_deeplink_filter
from filters import salesman_filter
from models import Salesman
from repositories import SaleRepository
from views import SaleTemporaryCodeSuccessfullyAppliedView, answer_view

router = Router(name=__name__)


@router.message(
    F.text,
    code_deeplink_filter,
    salesman_filter,
    StateFilter('*'),
)
async def on_scan_qr_code(
        message: Message,
        code: str,
        salesman: Salesman,
        sale_repository: SaleRepository,
) -> None:
    sale = await sale_repository.create(
        code=code,
        salesman_user_id=salesman.user_id,
    )
    view = SaleTemporaryCodeSuccessfullyAppliedView(sale)
    await answer_view(message, view)
