from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from exceptions.codes import CodeDoesNotExistError
from filters import (
    code_input_filter,
    user_is_admin_filter,
    user_is_salesman_filter,
)
from models import User
from repositories import GiftRepository, SaleRepository

__all__ = ('router',)

router = Router(name=__name__)


@router.message(
    F.chat.type == ChatType.PRIVATE,
    F.text == '📲 Ввести код вручную',
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter('*'),
)
async def on_ask_for_sale_temporary_code(message: Message) -> None:
    await message.answer('✏️ Введи код')


@router.message(
    F.chat.type == ChatType.PRIVATE,
    code_input_filter,
    or_f(
        user_is_salesman_filter,
        user_is_admin_filter,
    ),
    StateFilter('*'),
)
async def on_sale_temporary_code_input(
        message: Message,
        state: FSMContext,
        sale_repository: SaleRepository,
        gift_repository: GiftRepository,
        code: str,
        user: User,
) -> None:
    await state.clear()
    try:
        await gift_repository.activate_code(
            code=code,
            employee_user_id=message.from_user.id,
        )
    except CodeDoesNotExistError:
        await sale_repository.create_by_code(
            code=code,
            employee_user_id=user.id,
        )
